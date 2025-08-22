from django.forms.models import model_to_dict

def model_to_dict_with(model):
    data = model_to_dict(model)
    data["create_time"] = model.create_time.strftime("%Y-%m-%d %H:%M:%S")
    data["uid"] = str(model.uid)
    return data