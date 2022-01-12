import datetime
from flask import redirect, url_for, render_template, request, session, flash, Blueprint
from webApp.database import DatabaseSQL
from util import generateRandomNumberIngredient, generateRandomNumberKeyword, generateRandomNumberRecipe, timeStringToTimedelta, parseString

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

        # Check if user already exists in database
        cursor = sqlDB.dbCursor
        emailTuple = (email, )
        query = "SELECT * FROM users WHERE UserEmail = %s"
        cursor.execute(query, emailTuple)
        userDB = cursor.fetchall()

        # Check if user exists
        if userDB:
            userPass = userDB[0][2]

            # If user exists, check if inserted the correct password
            if userPass == password:
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
            flash("Not authorized!")
            return redirect(url_for("main_bp.queries"))

    # Check if user want to search recipe by id
    idButton = request.form.get("idSearchButton")
    if idButton is not None:
        if request.method == 'POST':
            recipeId = request.form["recipeIDtb"]
            session["recipeId"] = recipeId
            return redirect(url_for("main_bp.recipe"))

    # Check if user want to search recipe by name
    nameButton = request.form.get("nameButton")
    if nameButton is not None:
        if request.method == 'POST':
            recipeName = request.form["nameSearch"]
            cursor = sqlDB.dbCursor
            recipeNameTuple = (recipeName,)
            query = "select * from recipes where RecipeName = %s"
            cursor.execute(query, recipeNameTuple)
            recipeList = cursor.fetchall()
            return render_template("viewAll.html", values=recipeList)

    # Check if user want to search recipe by keyword
    keywordSearch = request.form.get("keywordSearch")
    if keywordSearch is not None:
        if request.method == 'POST':
            recipeKeyword = request.form["keywordTb"]
            cursor = sqlDB.dbCursor
            recipeKeywordTuple = (recipeKeyword,)
            query = "SELECT * FROM recipes INNER JOIN keywordstorecipes ON recipes.RecipeID = KeywordsToRecipes.RecipeID INNER JOIN keywords ON KeywordsToRecipes.KeywordID = keywords.KeywordID WHERE KeywordName = %s"
            cursor.execute(query, recipeKeywordTuple)
            recipeList = cursor.fetchall()
            return render_template("viewAll.html", values=recipeList)

    # Check if user want to search recipe by servings
    servingsSearch = request.form.get("servingsSearch")
    if servingsSearch is not None:
        if request.method == 'POST':
            servings = request.form["servingsTb"]
            cursor = sqlDB.dbCursor
            servingsTuple = (servings,)
            query = "select * from recipes where RecipeServings = %s"
            cursor.execute(query, servingsTuple)
            recipeList = cursor.fetchall()
            return render_template("viewAll.html", values=recipeList)

    # Check if user want to search recipe by nutrient value
    searchCalories = request.form.get("searchCalories")
    if searchCalories is not None:
        if request.method == 'POST':
            caloriesValue = request.form["nutrientTb"]
            cursor = sqlDB.dbCursor
            caloriesTuple = (caloriesValue,)
            query = "SELECT * FROM  recipes INNER JOIN NutritionQuantity ON recipes.RecipeID = NutritionQuantity.RecipeID WHERE calories < %s"
            cursor.execute(query, caloriesTuple)
            recipeList = cursor.fetchall()
            return render_template("viewAll.html", values=recipeList)

    # Check if user want to search recipe by its rating
    ratingSearch = request.form.get("aggregatedSearch")
    if ratingSearch is not None:
        if request.method == 'POST':
            recipeRating = request.form["ratingSearch"]
            cursor = sqlDB.dbCursor
            servingsTuple = (recipeRating,)
            query = "SELECT * FROM recipes WHERE AggregatedRating = %s"
            cursor.execute(query, servingsTuple)
            recipeList = cursor.fetchall()
            return render_template("viewAll.html", values=recipeList)

    # Check if user want to search top 10 fast recipe with the highest rating
    specialQuery1 = request.form.get("specialQuery1")
    if specialQuery1 is not None:
        cursor = sqlDB.dbCursor
        query = "select * from ( select * from recipes order by AggregatedRating DESC LIMIT 10) as T order by TotalTime"
        cursor.execute(query)
        recipeList = cursor.fetchall()
        return render_template("viewAll.html", values=recipeList)

    # Check if user want to search all recipes with rating above average
    specialQuery2 = request.form.get("specialQuery2")
    if specialQuery2 is not None:
        cursor = sqlDB.dbCursor
        query = "select * from recipes group by RecipeID having AggregatedRating >= ( select avg(AggregatedRating) from recipes)"
        cursor.execute(query)
        recipeList = cursor.fetchall()
        return render_template("viewAll.html", values=recipeList)

    # Check if user want to give keyword, and get all recipes with each nutrient bellow average
    keywordButtonSpecial = request.form.get("keywordButtonSpecial")
    if keywordButtonSpecial is not None:
        if request.method == 'POST':
            sqlDB.dbConnection.commit() # for fetchall
            keywordSpecial = request.form["keywordTextBoxSpecial"]
            keywordTuple = (keywordSpecial,)
            cursor = sqlDB.dbCursor
            query = """select * from recipes inner join nutritionquantity on recipes.recipeID = nutritionquantity.recipeID inner join KeywordsToRecipes on recipes.recipeID = KeywordsToRecipes.recipeID inner join keywords on KeywordsToRecipes.KeywordID = keywords.keywordID having calories <=( select avg(calories) from nutritionQuantity) and fatcontent <= ( select avg(fatcontent) from nutritionQuantity)and SaturatedFatContent <= ( select avg(SaturatedFatContent) from nutritionQuantity)and CholesterolContent  <= ( select avg(CholesterolContent ) from nutritionQuantity)and SodiumContent <= ( select avg(SodiumContent) from nutritionQuantity)and CarbohydrateContent <= ( select avg(CarbohydrateContent) from nutritionQuantity)and FiberContent <= ( select avg(FiberContent) from nutritionQuantity)and SugarContent <= ( select avg(SugarContent) from nutritionQuantity) and ProteinContent <= ( select avg(ProteinContent) from nutritionQuantity) and KeywordName = %s"""
            cursor.execute(query, keywordTuple)
            recipeList = cursor.fetchall()
            return render_template("viewAll.html", values=recipeList)

    return render_template("queries.html")


# Define screen to show all items
@main_bp.route('/viewAll', methods=["POST", "GET"])
def viewAll():

    # Make sure there is a list to show, otherwise redirect back
    if "recipeList" in session:
        return render_template('viewAll.html', values=session["recipeList"])
    else:
        return redirect(url_for("main_bp.queries"))


# Define a recipe screen route
@main_bp.route("/recipe", methods=["POST", "GET"])
def recipe():

    # Check if user want to rate a recipe
    ratingButton = request.form.get("ratingButton")
    if ratingButton is not None and "recipeId" in session and "recipe" in session and request.method == "POST":
        userRating = int(request.form["ratingTextBox"])
        recipeRating = session["recipe"][8]
        reviewCount = session["recipe"][6]

        # Calculate new recipe rating and number of votes
        recipeRating = recipeRating / reviewCount
        recipeNewRating = (recipeRating * reviewCount + userRating) / reviewCount + 1
        recipeNewCount = reviewCount + 1

        # Update new info in database
        cursor = sqlDB.dbCursor
        data = (recipeNewRating, recipeNewCount, session["recipeId"])
        query = """UPDATE recipes SET AggregatedRating = %s, ReviewCount = %s WHERE RecipeID = %s"""
        cursor.execute(query, data)
        sqlDB.dbConnection.commit()
        flash("Rating submitted!")
        return redirect(url_for("main_bp.recipe"))

    # Check if user want to delete a recipe
    deleteButton = request.form.get("deleteButton")
    if deleteButton is not None and "recipeId" in session and request.method == "POST":

        # Check if user has permissions
        if "email" in session:

            cursor = sqlDB.dbCursor
            query = "SET sql_safe_updates=0"
            cursor.execute(query)
            recipeIdTuple = (session["recipeId"],)
            query = "DELETE ingredients, keywords, keywordstorecipes, nutritionquantity, recipes, recipestoingredients FROM recipes inner join recipestoingredients on recipes.RecipeID = recipestoingredients.RecipeID inner join ingredients on recipestoingredients.IngredientID = ingredients.IngredientID inner join nutritionquantity on recipes.RecipeID = nutritionquantity.RecipeID inner join keywordstorecipes on recipes.RecipeID = keywordstorecipes.RecipeID inner join keywords on keywordstorecipes.KeywordID = keywords.KeywordID WHERE recipes.RecipeID = %s"
            cursor.execute(query, recipeIdTuple)
            query = "SET sql_safe_updates=1"
            cursor.execute(query)
            sqlDB.dbConnection.commit()

            # Remove all data from session if item deleted
            session.pop("recipeId", None)
            temp = session["email"]
            session.clear()
            session["email"] = temp

            flash("Recipe deleted successfully!")
            return redirect(url_for("main_bp.recipe"))

        # User doesn't have permissions to delete
        else:
            flash("Not authorized!")
            return redirect(url_for("main_bp.recipe"))

    # Check if user want to update a recipe
    updateButton = request.form.get("updateButton")
    if updateButton is not None and "recipeId" in session and request.method == "POST":

        # Check if user has permissions
        if "email" in session:
            return redirect(url_for("main_bp.updateRecipe"))

        # User doesn't have permissions to update
        else:
            flash("Not authorized!")
            return redirect(url_for("main_bp.recipe"))

    # Check if a single recipe is search
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

        # Get recipe ingredients amount
        query = "select RecipeIngredientQuantities from recipes inner join RecipesToIngredients on recipes.RecipeID = RecipesToIngredients.RecipeID inner join Ingredients on RecipesToIngredients.IngredientID = Ingredients.IngredientID where recipes.RecipeID = %s"
        cursor.execute(query, recipeIdTuple)
        ingredientsAmount = cursor.fetchall()

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

        # Serialize recipe to recipeList (from timedelta to str) and cache it
        recipeList: list = list()
        for i in range(len(recipe)):
            # Check if its recipe cook/prep time then convert it
            if i == 2 or i == 3:
                recipeList.append(str(recipe[i]))
                continue
            # Check if its total time then add it from previous calculation
            if i == 4:
                recipeList.append(totalTime)
                continue
            recipeList.append(recipe[i])

        session["recipe"] = recipeList
        session["ingredientsList"] = ingredientsList
        session["ingredientsAmount"] = ingredientsAmount

        # Show all information on recipe
        return render_template("recipe.html", recipeName=recipe[1], aggregatedRating=recipe[8], reviewCount=recipe[6],
                               recipeDescription=recipe[5], ingredientsList=ingredientsList, recipeInstructions=recipe[9],
                               recipePrep=str(recipe[3]), ingredientsAmount=ingredientsAmount,
                               recipeCook=str(recipe[2]), recipeTotal=totalTime, keywordsList=keywordsList,
                               calories=nutrientsList[0][1], fat=nutrientsList[0][2], saturatedFat=nutrientsList[0][3],
                               cholesterol=nutrientsList[0][4], sodium=nutrientsList[0][5], carbohydrate=nutrientsList[0][6],
                               fiber=nutrientsList[0][7], sugar=nutrientsList[0][8], protein=nutrientsList[0][9])

    return render_template("recipe.html")


# Define an add recipe screen route
@main_bp.route("/addRecipe", methods=["POST", "GET"])
def addRecipes():

    # Check if user inserted data to form, grab it
    if request.method == "POST":
        recipeId = generateRandomNumberRecipe(MIN, MAX)
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
                keywordId = generateRandomNumberKeyword(MIN, MAX)
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
                ingredientId = generateRandomNumberIngredient(MIN, MAX)
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

    # Check if user viewing a recipe to update it
    if "recipeId" in session and "recipe" in session and "nutrientsList" in session:
        recipeId = session["recipeId"]
        recipeName = session["recipe"][1]
        recipeDescription = session["recipe"][5]
        servings = session["recipe"][7]
        instructions = session["recipe"][9]
        calories = session["nutrientsList"][0][1]
        fatContent = session["nutrientsList"][0][2]
        saturatedFatContent = session["nutrientsList"][0][3]
        cholesterolContent = session["nutrientsList"][0][4]
        sodiumContent = session["nutrientsList"][0][5]
        carbohydrateContent = session["nutrientsList"][0][6]
        fiberContent = session["nutrientsList"][0][7]
        sugarContent = session["nutrientsList"][0][8]
        proteinContent = session["nutrientsList"][0][9]
        prepTime = session["recipe"][2]
        cookTime = session["recipe"][3]

        # Calculate recipe total time
        recipeCook = cookTime
        recipeCookDelta = timeStringToTimedelta(recipeCook)
        recipePrep = prepTime
        recipePrepDelta = timeStringToTimedelta(recipePrep)
        recipeTotal = recipePrepDelta + recipeCookDelta
        recipeTotal = recipeTotal - datetime.timedelta(days=recipeTotal.days)  # remove days

        # Check if post method was used -  user tried to update
        if request.method == "POST":
            recipeName = request.form["recipeName"]
            recipeDescription = request.form["description"]
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
            recipeTotal = recipeTotal - datetime.timedelta(days=recipeTotal.days)  # remove days

            cursor = sqlDB.dbCursor
            data = (recipeName, recipePrepDelta, recipeCookDelta, recipeTotal, recipeDescription, recipeServings, recipeInstructions, calories, fat, saturatedFat, cholesterol, sodium, carbohydrate, fiber, sugar, protein, recipeId)
            query = """UPDATE recipes INNER JOIN nutritionquantity ON recipes.RecipeID = nutritionquantity.recipeID SET RecipeName = %s, PrepTime = %s, CookTime = %s, TotalTime = %s, TheDescription = %s, RecipeServings = %s, RecipeInstructions = %s, Calories = %s, FatContent = %s, SaturatedFatContent = %s, CholesterolContent = %s, SodiumContent = %s, CarbohydrateContent = %s, FiberContent = %s, SugarContent = %s, ProteinContent = %s WHERE recipes.RecipeID = %s"""
            cursor.execute(query, data)

            # Submit all changes into database
            sqlDB.dbConnection.commit()
            flash("Recipe updated successfully!")
            return render_template("recipeUpdate.html")

        # Otherwise, user didn't update show all current data in form
        else:
            return render_template("recipeUpdate.html", recipeName=recipeName, recipeDescription=recipeDescription,
                                   instructions=instructions, prepTime=prepTime, cookTime=cookTime, servings=servings,
                                   calories=calories, fatContent=fatContent, saturatedFatContent=saturatedFatContent,
                                   cholesterolContent=cholesterolContent, sodiumContent=sodiumContent,
                                   carbohydrateContent=carbohydrateContent, fiberContent=fiberContent,
                                   sugarContent=sugarContent, proteinContent=proteinContent)
    else:
        flash("Not authorized!")

    return render_template("recipeUpdate.html")

