from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin

def update_views(request, object):
    context = {}
    hit_count = get_hitcount_model().objects.get_for_object(object)
    hits = hit_count.hits
    hitcontext = context["hitcount"] = {"pk": hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)

    if hit_count_response.hit_counted:
        hits = hits+1
        hitcontext["hitcounted"] = hit_count_response.hit_counted
        hitcontext["hit_message"] = hit_count_response.hit_message
        hitcontext["total_hits"] = hits

def filter_curse_words(text):
    curse_words = ['fuck','shit','bitch','damn','hell','ass','bastard','dick','crap','piss','slut','whore','cunt','cock','pussy','motherfucker','tits','bastard','asswipe','bollocks','bugger','chode','clit','cocksucker','coon','cum','dildo','fag','faggot','jizz','knob','minge','nigger','niggas','prick','pube','pussy','queer','rimjob','scrote','skank','slag','spunk','twat','wank','arsehole','ballbag','bellend','bloody']  # replace with your actual words
    words = text.split()
    filtered_words = []

    for word in words:
        # Check if word is a curse word (case-insensitive)
        if word.lower() in [c.lower() for c in curse_words]:
            word = '*' * len(word)
        filtered_words.append(word)

    return ' '.join(filtered_words)