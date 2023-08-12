import pandas
from event_extraction_.main import *
output=pandas.read_csv('labels.csv')


"""preprocessing on results and labeled data for matching and evaluating"""


# my results events and subjects

def get_sub_event_id_from_result(final_results):
    dialog_id_results = []
    events_results = []
    subjects_results = []
    for i in final_results:
        b = i[0]
        print(b)
        dialog_id_results.append(i[1])
        print("events ==> ", str(b[0][0]), " ||| subjects ==> ", str(b[0][1]), " ||| dialog number ==> ", i[1])
        print("\n")
        events_results.append(b[0][0])
        subjects_results.append(b[0][1])
    return dialog_id_results, events_results, subjects_results

dialog_id_results, events_results, subjects_results = get_sub_event_id_from_result(final_results)




#getting events and subjects from labeled dataset
def get_sub_event_id_from_labeledData(output):
    events=[]
    subjects=[]
    dialog_id=[]
    subjects_no_resolution=[]
    for i in range(len(output)):
        events.append(output["events"][i])
        subjects.append(output["subjects"][i])
        dialog_id.append(output["dialog_id"][i])
        subjects_no_resolution.append(output["subjects_no_resolution"][i])
    for i in range(len(events)):
        print("events ==> ",events[i], " ||| subjects ==> ",subjects[i]," ||| subjects befor resolution ==> ",subjects_no_resolution[i]," ||| dialog number ==> ",dialog_id[i])
        print("\n")
    return dialog_id,events,subjects,subjects_no_resolution

dialog_id,events,subjects,subjects_no_resolution = get_sub_event_id_from_labeledData(output)

# preprocessing on labeled dataset for easier matching with results



def preprocessing_on_labeledData(events,subjects,subjects_no_resolution):
    events_preprocessed = []
    subjects_preprocessed = []
    subjects_no_resolution_preprocessed = []
    for i, j in enumerate(events):

        # sentence has more one events like 'passed exam,married' transformed to [passed exam,married]
        if "," in str(events[i]):
            b = []
            c = events[i]
            b.append(c[:c.find(",")])
            b.append(c[c.find(",") + 1:])

            events_preprocessed.append(b)
        if "," not in str(events[i]):
            events_preprocessed.append([events[i]])

        # the same for subjects after resolution
    for i, j in enumerate(subjects):
        if "," in str(subjects[i]):
            d = []
            c = subjects[i]
            d.append(c[:c.find(",")])
            d.append(c[c.find(",") + 1:])

            subjects_preprocessed.append(d)
        if "," not in str(subjects[i]):
            subjects_preprocessed.append([subjects[i]])

        # the same for subjects befor resolution
    for i, j in enumerate(subjects_no_resolution):
        if "," in str(subjects_no_resolution[i]):
            e = []
            c = subjects_no_resolution[i]
            e.append(c[:c.find(",")])
            e.append(c[c.find(",") + 1:])

            subjects_no_resolution_preprocessed.append(e)

        if "," not in str(subjects_no_resolution[i]):
            subjects_no_resolution_preprocessed.append([subjects_no_resolution[i]])
    return events_preprocessed,subjects_preprocessed,subjects_no_resolution_preprocessed

events_preprocessed,subjects_preprocessed,subjects_no_resolution_preprocessed = preprocessing_on_labeledData(events,subjects,subjects_no_resolution)



# all this for subjects results after pronoun resolution

# we and they resolution maybe get subjects like "yara and hadia" will transformed to ['yara','hadia']

def preprocessing_on_resultSubjects(subjects_results):
    subjects_results_preprocessed = []
    for i, j in enumerate(subjects_results):

        if " and " in str(subjects_results[i]):
            b = []
            c = subjects_results[i][0]
            b.append(c[:c.find(" and ")])
            b.append(c[c.find(" and ") + 5:])
            b.sort()
            subjects_results_preprocessed.append(b)
        else:
            subjects_results_preprocessed.append(subjects_results[i])

        # subjects like joy's father .. my results return it like [('joy','father')] so will transformed to ['joy father']
        for k, l in enumerate(subjects_results[i]):
            if isinstance(subjects_results[i][k], tuple) == True:
                c = subjects_results[i][k]
                subjects_results_preprocessed[i][k] = [str(c[0]) + " " + str(c[1])]
            else:
                subjects_results_preprocessed[i][k] = subjects_results_preprocessed[i][k]
    return subjects_results_preprocessed

subjects_results_preprocessed = preprocessing_on_resultSubjects(subjects_results)


def get_subject_result_befor_resolution_withoutID(subject_result_befor_resolution):
    subject_result_befor_resolution_withoutID = []
    for i in subject_result_befor_resolution:
        b = i[0]
        subject_result_befor_resolution_withoutID.append(b)
    return subject_result_befor_resolution_withoutID
subject_result_befor_resolution_withoutID = get_subject_result_befor_resolution_withoutID(subject_result_befor_resolution)


def preprocessing_on_subject_result_befor_resolution_withoutID(subject_result_befor_resolution_withoutID):
    for i, j in enumerate(subject_result_befor_resolution_withoutID):
        for k, l in enumerate(subject_result_befor_resolution_withoutID[i]):
            if k <= len(subject_result_befor_resolution_withoutID[i]):

                if isinstance(l, tuple) == True:
                    subject_result_befor_resolution_withoutID[i][k] = [str(l[0]) + " " + str(l[1])]
                else:
                    subject_result_befor_resolution_withoutID[i][k] = subject_result_befor_resolution_withoutID[i][k]
    return subject_result_befor_resolution_withoutID

subject_result_befor_resolution_withoutID = preprocessing_on_subject_result_befor_resolution_withoutID(
    subject_result_befor_resolution_withoutID)



#fill lists with None values with the same labeled data long
def fill_with_null(dialog_id):
    null_subject=[]
    null_subject_befor_resolution=[]
    null_events=[]
    for i,j in enumerate(dialog_id):
        null_subject.append([['None'],dialog_id[i]])
        null_events.append([['None'],dialog_id[i]])
        null_subject_befor_resolution.append([['None'],dialog_id[i]])
    return null_subject,null_events,null_subject_befor_resolution

null_subject,null_events,null_subject_befor_resolution = fill_with_null(dialog_id)


def fill_null_with_value_of_subjects_results(null_subject,subjects_results_preprocessing):
    for i,j in enumerate(null_subject):
        for k,l in enumerate(subjects_results_preprocessing):
            if str(dialog_id_results[k]).strip() == str(null_subject[i][1]).strip():
                null_subject[i][0]=subjects_results_preprocessing[k]
                null_events[i][0]=events_results[k]
                null_subject_befor_resolution[i][0]=subject_result_befor_resolution_withoutID[k]
    return null_subject,null_events,null_subject_befor_resolution
final_subjects_res_preprocessing,final_events_res_preprocessing,final_subject_befor_resolution_res_preprocessing = fill_null_with_value_of_subjects_results(null_subject,subjects_results_preprocessed)



# compar null_subject with subjects_ from labeled data
# compar null_event with events_ from labeled data

def evaluation(dialog_id=[], final_subjects_res_preprocessing=[], subjects_preprocessed=[]):
    count_true_negative = 0
    count_true_positive = 0
    count_false_positive = 0
    count_false_negative = 0
    a_list = set()
    b_list = set()
    c_list = set()
    d_list = set()
    o_list = set()

    count_other = 0

    for i, j in enumerate(dialog_id):
        if str(dialog_id[i]) == str(final_subjects_res_preprocessing[i][1]):
            for k, l in enumerate(subjects_preprocessed[i]):
                for c, m in enumerate(final_subjects_res_preprocessing[i][0]):
                    if str(subjects_preprocessed[i][k]).lower().strip() == str(
                            final_subjects_res_preprocessing[i][0][c]).lower().strip() and str(
                            subjects_preprocessed[i][k]).lower().strip() == "none" and str(
                            final_subjects_res_preprocessing[i][0][c]).lower().strip() == "none":
                        # print(subjects_[i][k]," ....... ",null_subject[i][0][c],"........ ",dialog_id[i])
                        a_list.add(dialog_id[i])
                        count_true_negative += 1

    for i, j in enumerate(dialog_id):
        if dialog_id[i] not in a_list:
            if str(dialog_id[i]) == str(final_subjects_res_preprocessing[i][1]):
                for k, l in enumerate(subjects_preprocessed[i]):
                    for c, m in enumerate(final_subjects_res_preprocessing[i][0]):
                        if str(subjects_preprocessed[i][k]).lower().strip() == str(
                                final_subjects_res_preprocessing[i][0][c]).lower().strip() and str(
                                subjects_preprocessed[i][k]).lower().strip() != "none" and str(
                                final_subjects_res_preprocessing[i][0][c]).lower().strip() != "none":
                            # print(subjects_[i][k]," ....... ",null_subject[i][0][c],"........ ",dialog_id[i])
                            count_true_positive += 1
                            b_list.add(dialog_id[i])

    for i, j in enumerate(dialog_id):
        if dialog_id[i] not in a_list and dialog_id[i] not in b_list:
            if str(dialog_id[i]) == str(final_subjects_res_preprocessing[i][1]):
                for k, l in enumerate(subjects_preprocessed[i]):
                    for c, m in enumerate(final_subjects_res_preprocessing[i][0]):
                        if str(subjects_preprocessed[i][k]).lower().strip() != str(
                                final_subjects_res_preprocessing[i][0][c]).lower().strip() and str(
                                subjects_preprocessed[i][k]).lower().strip() == "none" and str(
                                final_subjects_res_preprocessing[i][0][c]).lower().strip() != "none":
                            # print(subjects_[i][k]," ....... ",null_subject[i][0][c],"........ ",dialog_id[i])
                            count_false_positive += 1
                            c_list.add(dialog_id[i])

    for i, j in enumerate(dialog_id):
        if dialog_id[i] not in a_list and dialog_id[i] not in b_list and dialog_id[i] not in c_list:
            if str(dialog_id[i]) == str(final_subjects_res_preprocessing[i][1]):
                for k, l in enumerate(subjects_preprocessed[i]):
                    for c, m in enumerate(final_subjects_res_preprocessing[i][0]):
                        if str(subjects_preprocessed[i][k]).lower().strip() != str(
                                final_subjects_res_preprocessing[i][0][c]).lower().strip() and str(
                                subjects_preprocessed[i][k]).lower().strip() != "none" and str(
                                final_subjects_res_preprocessing[i][0][c]).lower().strip() == "none":
                            # print(subjects_[i][k]," ....... ",null_subject[i][0][c],"........ ",dialog_id[i])
                            count_false_negative += 1
                            d_list.add(dialog_id[i])

    for i, j in enumerate(dialog_id):
        if dialog_id[i] not in a_list and dialog_id[i] not in b_list and dialog_id[i] not in c_list and dialog_id[
            i] not in d_list:
            if str(dialog_id[i]) == str(final_subjects_res_preprocessing[i][1]):
                for k, l in enumerate(subjects_preprocessed[i]):
                    for c, m in enumerate(final_subjects_res_preprocessing[i][0]):
                        if (str(subjects_preprocessed[i][k]).lower().strip() != str(
                                final_subjects_res_preprocessing[i][0][c]).lower().strip()) and (
                                str(subjects_preprocessed[i][k]).lower().strip() != "none") and (
                                str(final_subjects_res_preprocessing[i][0][c]).lower().strip() != "none"):
                            # print(subjects_[i][k]," ....... ",null_subject[i][0][c],"........ ",dialog_id[i])
                            count_other += 1
                            o_list.add(dialog_id[i])

    return a_list, b_list, c_list, d_list, o_list


# compare between subjects_ which is the labeled and preprocessed subject in data  .. with subject results after fill empty results
# with Null value

a_list, b_list, c_list, d_list, o_list = evaluation(dialog_id, final_subjects_res_preprocessing, subjects_preprocessed)
print("true_negative for subjects with pronoun resolution  : ", len(a_list))
print("true_positive for subjects with pronoun resolution  : ", len(b_list))
print("false_positive for subjects with pronoun resolution  : ", len(c_list) + len(o_list))
print("false_negative for subjects with pronoun resolution  : ", len(d_list))
# Recall = TruePositives / (TruePositives + FalseNegatives)
# Precision = TruePositives / (TruePositives + FalsePositives)
print("Precision ", (float)(len(b_list) / (float)((len(b_list)) + (len(c_list) + len(o_list)))))
print("Recall ", (float)(len(b_list) / (float)(len(b_list) + len(d_list))))




a_list,b_list,c_list,d_list,o_list=evaluation(dialog_id,final_subject_befor_resolution_res_preprocessing,subjects_no_resolution_preprocessed)
print("true_negative for subjects befor pronoun resolution  : ",len(a_list))
print("true_positive for subjects befor pronoun resolution  : ",len(b_list))
print("false_positive for subjects befor pronoun resolution  : ",len(c_list)+len(o_list))
print("false_negative for subjects befor pronoun resolution  : ",len(d_list))
#Recall = TruePositives / (TruePositives + FalseNegatives)
#Precision = TruePositives / (TruePositives + FalsePositives)
print("Precision ",(float)(len(b_list)/(float)((len(b_list))+(len(c_list)+len(o_list)))))
print("Recall ",(float)(len(b_list)/(float)(len(b_list)+len(d_list))))



a_list, b_list, c_list, d_list, o_list = evaluation(dialog_id, final_events_res_preprocessing, events_preprocessed)
print("true_negative for events  : ", len(a_list))
print("true_positive for events  : ", len(b_list))
print("false_positive for events  : ", len(c_list) + len(o_list))
print("false_negative for events  : ", len(d_list))
# Recall = TruePositives / (TruePositives + FalseNegatives)
# Precision = TruePositives / (TruePositives + FalsePositives)
print("Precision ", (float)(len(b_list) / (float)((len(b_list)) + (len(c_list) + len(o_list)))))
print("Recall ", (float)(len(b_list) / (float)(len(b_list) + len(d_list))))