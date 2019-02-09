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
        # length = len(list(d.keys()))
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
        # t = "" + str(d[name])
        # keys = list(d.keys())
        d.close()
        return render_template("index.html", rosebud = "Submitted! Thank you!")
    return render_template("index.html")

@app.route("/tree", methods=["GET","POST"])
def treeeee():
    no_results_yet = True
    if request.method == "POST":
        name = request.form['nameInput2']
        d = shelve.open('test_shelf.db')
        grandmother = []
        coparents = []
        hasfamily = False
        no_results_yet = False
        # keys = list(d.keys())

        if name in d:
            hasfamily = True
            roses2 = list(d[name]["roses"].keys())
            buds2 = list(d[name]["buds"].keys())

            for i in roses2:
                if i in d and i != name:
                    grandmother += list(d[i]["roses"].keys())

            for i in buds2:
                if i in d and i != name:
                    coparents += list(d[i]["roses"].keys())

            bbuds = "Your rosebuds are " + ", ".join(roses2)
            rroses = "Your buds are " + ", ".join(buds2)
            ggrand = "Your grandparents are " + ", ".join(grandmother)
            coparent = "Your coparents are " + ", ".join(coparents)
            return render_template("mytree.html", bbuds = bbuds, roses = rroses, ggrand = ggrand, coparent = coparent, hasfamily = hasfamily, no_results_yet = no_results_yet)
        else:
            notThere = False
            return render_template("mytree.html", notThere = notThere, no_results_yet = no_results_yet)
    return render_template("mytree.html", no_results_yet = no_results_yet)