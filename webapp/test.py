from flask import Flask, render_template_string
from wtforms import Form
from wtforms.fields.html5 import DecimalRangeField


app = Flask(__name__)
app.config['DEBUG'] = True

TPL = '''
<!DOCTYPE html>
<html>
<head>
<script>
function outputUpdate(age) {
    document.querySelector('#selected-age').value = age;
}
</script>
</head>
<body>
<form>
    <p>
       {{ form.age.label }}:
       {{ form.age(min=0, max=100, oninput="outputUpdate(value)") }}
       <output for="age" id="selected-age">{{ form.age.data }}</output>
    </p>
</form>
</body>
</html>
'''

class TestForm(Form):
    age = DecimalRangeField('Age', default=0)


@app.route("/")
def home():
    form = TestForm(csrf_enabled=False)
    return render_template_string(TPL, form=form)


if __name__ == "__main__":
    app.run()
