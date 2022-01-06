import datetime
import json
from flask import redirect, url_for, render_template, request, session, flash, Blueprint
from webApp.database import DatabaseSQL
from util import generateRandomNumber, timeStringToTimedelta, parseString

MAX = 1000000
MIN = 1

# Define application blueprint
main_bp = Blueprint('main_bp', __name__)

sqlDB = DatabaseSQL()


# Define home screen route
@main_bp.route('/')
def home():
    return render_template("index.html")


# Define logout screen route
@main_bp.route("/logout")
def logout():
    # If user is connected, show message to user and pop user from session
    if "email" in session:
        flash(f"You have been logged out!", "info")
        session.pop("email", None)

    return redirect(url_for("main_bp.login"))


# Define login screen route
@main_bp.route('/login', methods=["POST", "GET"])
def login():
    # Check if post method was used
    if request.method == "POST":

        # Save user email and password inserted into form
        email = request.form.get('email')
        password = request.form.get('password')
        session.permanent = True

        # Check if user already exists in database - TODO: decide if need to reinitialize connection or not
        cursor = sqlDB.dbCursor
        emailTuple = (email, )
        query = "SELECT * FROM users WHERE UserEmail = %s"
        cursor.execute(query, emailTuple)
        userDB = cursor.fetchall()
        # currentUser = User.query.filter_by(_email=email).first()
        if userDB:
            userPass = userDB[0][2]

            # If user exists, check if inserted the correct password
            if userPass == password:
                # session["email"] = currentUser.getEmail()
                session["email"] = userDB[0][1]
                flash("Logged in successfully!")

            # Notify user inserted wrong password, redirect him back
            else:
                flash("Wrong password!")
                return render_template("login.html")

        # User not exists, add him to database
        else:
            flash("User not registered!")
            return redirect(url_for("main_bp.login"))

        return redirect(url_for("main_bp.user"))

    else:
        # Check if user is already logged in
        if "email" in session:
            flash("Already logged in!")
            return redirect(url_for("main_bp.user"))

        # User is not logged in
        return render_template("login.html")


# Define user panel screen route
@main_bp.route("/user", methods=["POST", "GET"])
def user():
    # If user is connected, redirect him to his page
    if "email" in session:
        user1 = session["email"]
        return render_template("user.html", email=user1)

    # If user not connected, redirect to login page
    else:
        flash("You are not logged in!")
        return redirect(url_for("main_bp.login"))


# Define queries screen route
@main_bp.route("/queries", methods=["POST", "GET"])
def queries():
    # Check if user want to add recipe
    addRecipe = request.form.get("addRecipe")
    if addRecipe is not None:
        # Check if user is registered(guest cant add recipe)
        if "email" in session:
            return redirect(url_for("main_bp.addRecipes"))

        else:
            flash("Not authorized")
            return redirect(url_for("main_bp.queries"))

    # Check if user want to search recipe by id
    idButton = request.form.get("idSearchButton")
    if idButton is not None:        # todo handle recipeID not found
        if request.method == 'POST':
            recipeId = request.form["recipeIDtb"]
            session["recipeId"] = recipeId
            return redirect(url_for("main_bp.recipe"))

    nameButton = request.form.get("nameButton")
    if nameButton is not None:
        # Check if user want to search recipe by name
        if request.method == 'POST':
            recipeName = request.form["nameSearch"]

    # Check if user want to search recipe by keyword
    keywordSearch = request.form.get("keywordSearch")
    if keywordSearch is not None:
        flash("Clicked on keyword search")
        # return redirect(url_for("main_bp.queries"))

    # Check if user want to search recipe by ingredient
    ingredientSearch = request.form.get("ingredientSearch")
    if ingredientSearch is not None:
        flash("Clicked on ingredient search")

    # Check if user want to search recipe by nutrient value
    nutrientSearch = request.form.get("nutrientSearch")
    if nutrientSearch is not None:
        flash("Clicked on nutrient search")

    # Check if user want to search recipe by its rating
    ratingSearch = request.form.get("aggregatedSearch")
    if ratingSearch is not None:
        # Check if user want to search recipe by rating
        if request.method == 'POST':
            recipeRating = request.form["ratingSearch"]
            cursor = sqlDB.dbCursor
            ratingTuple = (recipeRating,)
            query = "SELECT * FROM recipes WHERE AggregatedRating = %s"
            cursor.execute(query, ratingTuple)
            recipeList = cursor.fetchall()
            return render_template("viewAll.html", values=recipeList)
            # # Get recipe keywords
            # for recipe in recipeList:
            #     recipeIdTuple = (recipe[0],)
            #     query = "SELECT KeywordName FROM recipes INNER JOIN keywordstorecipes ON recipes.RecipeID = KeywordsToRecipes.RecipeID INNER JOIN keywords ON KeywordsToRecipes.KeywordID = keywords.KeywordID WHERE recipes.RecipeiD = %s"
            #     cursor.execute(query, recipeIdTuple)
            #     keywordsList = cursor.fetchall()
                # recipeList = json.dumps(recipeList[0], indent=4, sort_keys=True, default=str)
                # session["recipeList"] = recipeList
                # return render_template("viewAll.html", values=[recipeList, keywordsList])
            # return redirect(url_for("main_bp.viewAll"))

    viewRecipe = request.form.get("viewRecipe")
    if viewRecipe is not None:
        return redirect(url_for("main_bp.recipe", recipeId=viewRecipe))

        # recipeIndex = 0
        # nextRecipe = request.form.get("prevButton")
        # prevRecipe = request.form.get("nextButton")
        # isButtonGreyed = False
        # if nextRecipe is not None:
        #     if recipeIndex <= len(recipeList):
        #         recipeIndex += 1
        #     else:
        #         isButtonGreyed = True
        # if prevRecipe is not None:
        #     if recipeIndex <= 0:
        #         recipeIndex -= 1
        #     else:
        #         isButtonGreyed = True

        # recipeName = recipeList[recipeIndex][1]
        # recipeCook = str(recipeList[recipeIndex][2])
        # newRecipeCook = recipeCook.strftime("%H:%M:%S")
        # recipePrep = str(recipeList[recipeIndex][3])
        # recipeTotal = str(recipeList[recipeIndex][4])
        # recipeDescription = recipeList[recipeIndex][5]
        # reviewCount = recipeList[recipeIndex][6]
        # recipeServings = recipeList[recipeIndex][7]
        # aggregatedRating = recipeList[recipeIndex][8]
        # recipeInstructions = recipeList[recipeIndex][9]

        # redirect(url_for("main_bp.recipes", values=[recipeName, recipeCook, recipePrep, recipeTotal, recipeDescription,
        #                         reviewCount, recipeServings, aggregatedRating, recipeInstructions]))
        # return render_template("recipe.html", values=[recipeName, recipeCook, recipePrep, recipeTotal, recipeDescription,
        #                        reviewCount, recipeServings, aggregatedRating, recipeInstructions])

    return render_template("queries.html")


# Define screen to show all items
@main_bp.route('/viewAll', methods=["POST", "GET"])
def viewAll():
    if request.method == "POST":
        pass
    else:
        if "recipeList" in session:
            return render_template('viewAll.html', values=session["recipeList"])
        # Check if user want to see specific recipe
        recipeId = int(request.form.get("viewRecipe"))
        if recipeId is not None:
            return redirect(url_for("main_bp.recipe", recipeId=recipeId))


# Define a recipe screen route
@main_bp.route("/recipe", methods=["POST", "GET"])
def recipe():

    # Check if user want to delete a recipe
    deleteButton = request.form.get("deleteButton")
    if deleteButton is not None and "recipeId" in session and request.method == "POST": # todo remove all inglist,keylist,recipe,nutlist from session
        if "email" in session:
            cursor = sqlDB.dbCursor
            query = "SET sql_safe_updates=0"
            cursor.execute(query)

            recipeIdTuple = (session["recipeId"],)
            query = "DELETE ingredients, keywords, keywordstorecipes, nutritionquantity, recipes, recipestoingredients FROM recipes inner join recipestoingredients on recipes.RecipeID = recipestoingredients.RecipeID inner join ingredients on recipestoingredients.IngredientID = ingredients.IngredientID inner join nutritionquantity on recipes.RecipeID = nutritionquantity.RecipeID inner join keywordstorecipes on recipes.RecipeID = keywordstorecipes.RecipeID inner join keywords on keywordstorecipes.KeywordID = keywords.KeywordID WHERE recipes.RecipeID = %s"
            cursor.execute(query, recipeIdTuple)

            query = "SET sql_safe_updates=1"
            cursor.execute(query)

            session.pop("recipeId", None)
            sqlDB.dbConnection.commit()
            flash("Recipe deleted successfully!")
            return redirect(url_for("main_bp.recipe"))

        else:
            flash("Not authorized!")
            return redirect(url_for("main_bp.recipe"))

    # Check if user want to update a recipe
    updateButton = request.form.get("updateButton")
    if updateButton is not None and "recipeId" in session and request.method == "POST":
        return redirect(url_for("main_bp.updateRecipe"))

    if "recipeId" in session:
        recipeId = session["recipeId"]
        cursor = sqlDB.dbCursor
        recipeIdTuple = (recipeId,)

        # Get recipe information
        query = "SELECT * FROM recipes WHERE RecipeID = %s"
        cursor.execute(query, recipeIdTuple)
        recipe = cursor.fetchone()
        totalTime = str(recipe[3] + recipe[2])

        # Get recipe ingredients
        query = "SELECT IngredientName FROM recipes  INNER JOIN RecipesToIngredients ON recipes.RecipeID = RecipesToIngredients.RecipeID INNER JOIN Ingredients ON RecipesToIngredients.IngredientID = Ingredients.IngredientID WHERE recipes.RecipeiD = %s"
        cursor.execute(query, recipeIdTuple)
        ingredientsList = cursor.fetchall()

        # Get recipe keywords
        query = "SELECT KeywordName FROM recipes INNER JOIN keywordstorecipes ON recipes.RecipeID = KeywordsToRecipes.RecipeID INNER JOIN keywords ON KeywordsToRecipes.KeywordID = keywords.KeywordID WHERE recipes.RecipeiD = %s"
        cursor.execute(query, recipeIdTuple)
        keywordsList = cursor.fetchall()

        # Get recipe nutrients
        query = "SELECT * FROM nutritionquantity WHERE recipeID = %s"
        cursor.execute(query, recipeIdTuple)
        nutrientsList = cursor.fetchall()

        # Cache current recipe
        session["nutrientsList"] = nutrientsList
        session["keywordsList"] = keywordsList
        recipeList: list = recipe.copy()
        recipeList[2] = str(recipeList[2])
        recipeList[3] = str(recipeList[3])
        # session["recipe"] = recipe
        session["ingredientsList"] = ingredientsList

        return render_template("recipe.html", recipeName=recipe[1], aggregatedRating=recipe[8], reviewCount=recipe[6],
                               recipeDescription=recipe[5], ingredientsList=ingredientsList, recipeInstructions=recipe[9],
                               recipePrep=str(recipe[3]),
                               recipeCook=str(recipe[2]), recipeTotal=totalTime, keywordsList=keywordsList,
                               calories=nutrientsList[0][0], fat=nutrientsList[0][1], saturatedFat=nutrientsList[0][2],
                               cholesterol=nutrientsList[0][3], sodium=nutrientsList[0][4], carbohydrate=nutrientsList[0][5],
                               fiber=nutrientsList[0][6], sugar=nutrientsList[0][7], protein=nutrientsList[0][8])

    return render_template("recipe.html")


# Define an add recipe screen route
@main_bp.route("/addRecipe", methods=["POST", "GET"])
def addRecipes():

    # Check if post method was used
    if request.method == "POST":
        recipeId = generateRandomNumber(MIN, MAX)
        recipeName = request.form["recipeName"]
        keywordsList = parseString(request.form["keywords"])
        recipeDescription = request.form["description"]
        ingredientsList = parseString(request.form["ingredients"])
        amountList = parseString(request.form["amount"])
        recipeServings = int(request.form["servings"])
        recipeInstructions = request.form["instructions"]
        calories = float(request.form["calories"])
        fat = float(request.form["fatContent"])
        saturatedFat = float(request.form["saturatedFatContent"])
        cholesterol = float(request.form["cholesterolContent"])
        sodium = float(request.form["sodiumContent"])
        carbohydrate = float(request.form["carbohydrateContent"])
        fiber = float(request.form["fiberContent"])
        sugar = float(request.form["sugarContent"])
        protein = float(request.form["proteinContent"])
        recipeCook = request.form["cookTime"]
        recipeCookDelta = timeStringToTimedelta(recipeCook)
        recipePrep = request.form["prepTime"]
        recipePrepDelta = timeStringToTimedelta(recipePrep)
        recipeTotal = recipePrepDelta + recipeCookDelta
        recipeTotal = recipeTotal - datetime.timedelta(days=recipeTotal.days)   # remove days
        reviewCount = 0
        aggregatedRating = 0

        # Insert new data into recipes table
        cursor = sqlDB.dbCursor
        data = (recipeId, recipeName, recipeCookDelta, recipePrepDelta, recipeTotal, recipeDescription, reviewCount,
                recipeServings, aggregatedRating, recipeInstructions)
        query = "INSERT INTO db_workshop_V2.recipes VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(query, data)
        sqlDB.dbConnection.commit()

        # Insert new data into nutrients quantity table
        data = (recipeId, calories, fat, saturatedFat, cholesterol, sodium, carbohydrate,
                fiber, sugar, protein)
        query = "INSERT INTO nutritionquantity VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, data)
        sqlDB.dbConnection.commit()

        # Insert new data into keywords table(only new ones) and keywordsToRecipes
        for keyword in keywordsList:

            # Check if keyword already exists in database
            query = "SELECT KeywordID FROM keywords WHERE KeywordName = %s"
            keywordTuple = (keyword,)
            cursor.execute(query, keywordTuple)
            keywordId = cursor.fetchone()

            # If keyword exists in database we will get its keyword ID, otherwise it doesn't exist - generate id
            # Insert new keywords into keywords table
            if not keywordId:
                keywordId = generateRandomNumber(MIN, MAX)
                data = (keywordId, keyword)
                query = "INSERT INTO keywords VALUES (%s, %s)"
                cursor.execute(query, data)
                sqlDB.dbConnection.commit()
            # If found Id remove tuple
            else:
                keywordId = keywordId[0]

            # Insert new data into keywordsToRecipes table
            data = (recipeId, keywordId)
            query = "INSERT INTO keywordstorecipes VALUES (%s, %s);"
            cursor.execute(query, data)
            sqlDB.dbConnection.commit()

        # Insert new data into ingredients table(only new ones) and recipesToIngredients
        for index, ingredient in enumerate(ingredientsList):

            # Check if ingredient already exists in database
            query = "SELECT IngredientID FROM ingredients WHERE IngredientName = %s"
            ingredientTuple = (ingredient,)
            cursor.execute(query, ingredientTuple)
            ingredientId = cursor.fetchone()

            # If ingredient exists in database we will get its ingredient ID, otherwise it doesn't exist - generate id
            # Insert new ingredients into ingredients table
            if not ingredientId:
                ingredientId = generateRandomNumber(MIN, MAX)
                ingredientName = "\"" + ingredient + "\""
                data = (ingredientId, ingredientName)
                query = "INSERT INTO ingredients VALUES (%s, %s)"
                cursor.execute(query, data)
                sqlDB.dbConnection.commit()

            # If found Id remove tuple
            else:
                ingredientId = ingredientId[0]

            # Insert new data into recipesToIngredients table
            data = (recipeId, ingredientId, amountList[index])
            query = "INSERT INTO RecipesToIngredients VALUES (%s, %s, %s)"
            cursor.execute(query, data)
            sqlDB.dbConnection.commit()

        flash("Submitted recipe successfully!")

    return render_template("recipeAdd.html")


# Define an update recipe screen route
@main_bp.route("/updateRecipe", methods=["POST", "GET"])
def updateRecipe():
    if "recipeId" in session and "recipe" in session and "ingredientsList" in session and "keywordsList" in session and \
            "nutrientsList" in session:

        flash("Recipe updated successfully!")
        # for each text box check if values is different from db, if not continue, if yes change the to the new value
        # commit after all was fine
    else:
        flash("Not authorized!")
    return render_template("recipeUpdate.html")


# if want to pass short list in return redirect(url_for("main_bp.viewAll", values=recipeList))
# if its long list use session user1 = session["email"]
