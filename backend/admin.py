from flask import Blueprint, render_template

admin = Blueprint("admin", __name__)

@admin.route("/admin")
def homeAdmin():
    return render_template("admin/dashboard.html")