from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from forms import CafeForm, SearchForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
bootstrap = Bootstrap(app)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Define Cafe Table
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


@app.route("/", methods=["GET", "POST"])
def home():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        cafe_loc = request.form.get("search_item").title()
        result = Cafe.query.filter_by(location=cafe_loc).all()

        if result:
            flash(f"Cafes in {cafe_loc}:", 'no_error')
            return render_template("index.html", form=search_form,
                                   cafes=result, display_result=True)
        else:
            flash("No cafes found in this area.", 'error')
            return redirect(url_for('home'))

    return render_template("index.html", form=search_form)


@app.route("/cafes")
def get_all_cafes():
    all_cafes = Cafe.query.order_by(Cafe.name).all()
    return render_template('cafes.html', cafes=all_cafes)


@app.route("/add", methods=["GET", "POST"])
def post_new_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe = Cafe(
            name=request.form.get("name"),
            map_url=request.form.get("map_url"),
            img_url=request.form.get("img_url"),
            location=request.form.get("location"),
            has_sockets=bool(request.form.get("has_sockets")),
            has_toilet=bool(request.form.get("has_toilet")),
            has_wifi=bool(request.form.get("has_wifi")),
            can_take_calls=bool(request.form.get("can_take_calls")),
            seats=request.form.get("seats"),
            coffee_price=request.form.get("price")
            )
        db.session.add(new_cafe)
        db.session.commit()
        flash("New cafe added successfully!", 'no_error')
        return redirect(url_for('post_new_cafe'))
    return render_template('add_cafe.html', form=form)


@app.route("/delete/<int:cafe_id>")
def delete_post(cafe_id):
    cafe_to_delete = Cafe.query.get_or_404(cafe_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_cafes'))


@app.route("/edit/<int:cafe_id>", methods=["GET", "POST"])
def edit_cafe(cafe_id):
    cafe = Cafe.query.get_or_404(cafe_id)
    edit_cafe_form = CafeForm(obj=cafe)
    if edit_cafe_form.validate_on_submit():
        edit_cafe_form.populate_obj(cafe)
        db.session.commit()
        return redirect(url_for("get_all_cafes"))
    return render_template("add_cafe.html", form=edit_cafe_form, is_edit=True)


if __name__ == '__main__':
    app.run(debug=True)
