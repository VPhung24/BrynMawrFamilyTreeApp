from flask import Flask, render_template, flash, request, url_for, redirect, session
import MySQLdb
import MySQLdb.cursors
import shelve

app = Flask(__name__)
app.config["DEBUG"] = True

# d = shelve.open('test_shelf.db')
# familytree = {}

# familytree["vphung11"] = {"name": "vphung", "roses": [], "buds": ["taylor", "hh"]}
# d["vphung11"] = {"name": "viv", "roses": [], "buds": ["tony", "dana", "lola"]}
# d["vphung22"] = {"name": "phu", "roses": [], "buds": []}
# d.close()

@app.route("/", methods=["GET","POST"])
def hello_world():
    if request.method == "POST":
        d = shelve.open('test_shelf.db', writeback = True)
        length = len(list(d.keys()))
        name = request.form['nameInput']
        bud = request.form['budInput']
        rose = request.form['roseInput']

        # if person already exist than update
        if name in d:
            if rose != "":
                d[name]["roses"][rose] = 0
            if bud != "":
                d[name]["buds"][bud] = 0
        else:
            d[name] = {"name": name, "roses": {}, "buds": {}}
            if rose != "":
                d[name]["roses"][rose] = 0
            if bud != "":
                d[name]["buds"][bud] = 0
        t = "" + str(d[name])
        # keys = list(d.keys())
        d.close()
        return render_template("index.html", rosebud = t)
    return render_template("index.html")

@app.route("/tree", methods=["GET","POST"])
def treeeee():
    if request.method == "POST":
        name = request.form['nameInput2']
        d = shelve.open('test_shelf.db')
        roses2 = list(d[name]["roses"].keys())
        buds2 = list(d[name]["buds"].keys())
        grandmother = []
        coparents = []
        # keys = list(d.keys())

        for i in roses2:
            if i in d:
                grandmother += list(d[i]["roses"].keys())

        for i in buds2:
            if i in d:
                coparents += list(d[i]["roses"].keys())

        if name in d:
            t = "your rosebuds are " + str(roses2) + " and your buds are " + str(buds2) + "! Your grandparents are " + str(grandmother) + " and your coparents are " + str(coparents)
        else:
            t = "No current fam"

        # t = str(keys)
        return render_template("mytree.html", HelloWorld = t)
    return render_template("mytree.html")
