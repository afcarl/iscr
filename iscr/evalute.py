def average_precision(ret, ans):
    """
            ret: list of tuples [ (docname, score) ]
            ans: python dictionary with answer as keys
    """
    tp = [float(docID in ans) for docID, val in ret]

    precisions = []
    ans_count = 0
    for idx, (docID, val) in enumerate(ret):
        ans_count += tp[idx]
        precisions.append(ans_count / (idx + 1) * tp[idx])

    return (sum(precisions) / len(ans) if len(ans) else 0.)
