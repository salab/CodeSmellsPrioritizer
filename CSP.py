import csv
import operator
import re
import copy
import sys
from operator import attrgetter


#####################
# Parameters
#####################
result_file_name = 'Results.csv'


#####################
# Start process
#####################
def main(code_smell_file_name, ia_file_name, alpha=1, cut_point=40):
    code_smells = get_code_smells_from_csv_file(code_smell_file_name)
    code_smells.sort(key=lambda x: int(x.severity), reverse=True)
    scored_code_smells = calculate_cri(code_smells, ia_file_name, cut_point)
    scored_code_smells = calculate_ranking(scored_code_smells, alpha)
    scored_code_smells.sort(key=lambda x: x.ranking, reverse=True)
    write_code_smells_to_csv_file(scored_code_smells, result_file_name)
    print("Prioritizing completed !")


class CodeSmell(object):
    def __init__(self, id_number=None, severity=None, entity_name=None, package_name=None,
                 smell_type=None, ranking=0, cri=0, n_cri=0, n_severity=0):
        self.id_number = id_number
        self.ranking = ranking
        self.cri = cri
        self.severity = severity
        self.entity_name = entity_name
        self.package_name = package_name
        self.smell_type = smell_type
        self.matched = False
        self.n_cri = n_cri
        self.n_severity = n_severity


class ImpactAnalysis(object):
    def __init__(self, issue_id=None):
        self.issue_id = issue_id
        self.data = []


def write_code_smells_to_csv_file(code_smells, csv_file_name):
    code_smells.sort(key=operator.attrgetter('ranking'), reverse=True)
    csv_file = open(csv_file_name, 'wb')
    try:
        fieldnames = ('Id', 'Ranking', 'CRI', 'Severity', 'Entity Name', 'Package Name', 'Smell Type')
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        headers = dict((n, n) for n in fieldnames)
        writer.writerow(headers)
        for code_smell in code_smells:
            writer.writerow({'Id': code_smell.id_number,
                             'Ranking': code_smell.ranking,
                             'CRI': code_smell.cri,
                             'Severity': code_smell.severity,
                             'Entity Name': code_smell.entity_name,
                             'Package Name': code_smell.package_name,
                             'Smell Type': code_smell.smell_type,
                             })
    finally:
        csv_file.close()


def calculate_cri(code_smells, ia_file_name, cut_point):
    scored_code_smells = copy.deepcopy(code_smells)
    impact_analysis_input_file = open(ia_file_name, 'rU')
    impact_analyses = []
    rows = []
    try:
        reader = csv.reader(impact_analysis_input_file)
        for row in reader:
            rows.append(row)
    finally:
        impact_analysis_input_file.close()

    ia_result = None
    for row in rows:
        if not ia_result:
            ia_result = ImpactAnalysis(row[0])
        elif row[0] != ia_result.issue_id:
            impact_analyses.append(ia_result)
            ia_result = ImpactAnalysis(row[0])
        ia_result.data.append([row[1], row[2]])
    impact_analyses.append(ia_result)

    # Scoring
    for impact_analysis in impact_analyses:
        for ia_class_name in impact_analysis.data:
            # ignore [] and <> in impact analysis
            ia_class_name[0] = re.sub('\[\]', '', ia_class_name[0])
            while '<' in ia_class_name[0]:
                ia_class_name[0] = re.sub('<.[^<|>]*>', '', ia_class_name[0])

    for code_smell in scored_code_smells:
        code_smell_full_name = str(code_smell.package_name) + '.' + str(code_smell.entity_name)
        code_smell_full_name = code_smell_full_name.split('/')[-1]

        for impact_analysis in impact_analyses:
            if cut_point == 'all':
                length = len(impact_analysis.data)
            else:
                length = int(cut_point)

            for ia_class_name in impact_analysis.data[:length]:
                if code_smell_full_name == ia_class_name[0]:
                        code_smell.cri += float(ia_class_name[1])

    return scored_code_smells


def calculate_ranking(code_smells, alpha):
    scored_code_smells = copy.deepcopy(code_smells)
    max_cri = max(scored_code_smells, key=attrgetter('cri')).cri
    min_cri = min(scored_code_smells, key=attrgetter('cri')).cri
    max_severity = max(scored_code_smells, key=attrgetter('severity')).severity
    min_severity = min(scored_code_smells, key=attrgetter('severity')).severity
    for code_smell in scored_code_smells:
        if max_cri == min_cri:
            code_smell.n_cri = 0
        else:
            code_smell.n_cri = float((code_smell.cri - min_cri)) / float((max_cri - min_cri))
        code_smell.n_severity = (float(code_smell.severity) - float(min_severity)) / (float(max_severity) - float(min_severity))
        code_smell.ranking = (alpha * code_smell.n_cri) + ((1 - alpha) * code_smell.n_severity)
    return scored_code_smells


def get_code_smells_from_csv_file(csv_file_name):
    code_smells = []
    rows = []
    csv_input_file = open(csv_file_name, 'rU')
    try:
        next(csv_input_file)  # skip header row
        reader = csv.reader(csv_input_file)
        for row in reader:
            rows.append(row)
    finally:
        csv_input_file.close()

    for row in rows:
        code_smells.append(CodeSmell(row[0], row[1], row[2], row[3], row[4]))

    return code_smells


if __name__ == '__main__':
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 4:
        main(sys.argv[1], sys.argv[2], float(sys.argv[3]))
    elif len(sys.argv) == 5:
        main(sys.argv[1], sys.argv[2], float(sys.argv[3]), int(sys.argv[4]))
