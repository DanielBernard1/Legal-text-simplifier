from summac.model_summac import SummaCZS

model_CZS = SummaCZS(granularity="sentence", model_name="vitc")

MODALS = ["shall", "must", "may", "should", "will", "can", "could", "might"]

def get_modals(text):
    words = text.lower().split()
    modals_found = []
    for w in words:
        stripped = w.strip(".,;:")
        if stripped in MODALS:
            modals_found.append(stripped)
    return modals_found


def modal_flip_detected(original, candidate):
    return get_modals(original) != get_modals(candidate)


#faithful_min  = 0.316772 corrupted_max = -0.000896
#threshold = (0.316772 + (-0.000896)) / 2 = 0.315876 / 2 ≈ 0.158
#faithful_min  = 0.800545 corrupted_max = 0.002337
#threshold = (0.800545 + 0.002337) / 2 = 0.802882 / 2 ≈ 0.401
def is_faithful(original, candidate, threshold_foward = 0.16 , threshold_reverse = 0.4):
    has_modal_flip = modal_flip_detected(original, candidate)

    forward_score = model_CZS.score([original], [candidate])["scores"][0]
    reverse_score = model_CZS.score([candidate], [original])["scores"][0]
    forward_ok = False
    reverse_ok = False
    if forward_score >= threshold_foward: forward_ok = True
    if reverse_score >= threshold_reverse: reverse_ok = True

    faith = False
    if has_modal_flip==False and forward_ok and reverse_ok: faith=True

    return {
        "is_faithful": faith,
        "modal_flip": has_modal_flip,
        "forward_score": forward_score,
        "reverse_score": reverse_score,
    }
