
    # # Seeds the Database (admins only)
    # @app.route('/seedDB')
    # def seedDB():
    #     db.drop_all()
    #     db.create_all()
    #     tonkatsu = Meals(title='Tonkatsu Ramen', restaurant="Nikko's", description="This dish was a perfect bowl of ramen. The pork was cooked perfectly and the broth was good too.", tags="affordable, leftovers, Japanese", tryAgain="Yes", starRating="5")
    #     pasta = Meals(title='Seafood Pasta', restaurant="Olive Garden", description="The meal was good but there wasn't as much seafood as I was hoping for. Would feel like more value for the price if they added some more in.", tags="pricey, small portion size, Italian", tryAgain="Maybe", starRating="3")
    #     cupBop = Meals(title='Rock Bop', restaurant="Cup Bop", description="This dish was way too spicy for my taste! I could barely task any of the food because my mouth burned.", tags="Korean, spicy, noodles", tryAgain="No", starRating="1")
   
    #     db.session.add(tonkatsu)
    #     db.session.add(pasta)
    #     db.session.add(cupBop)
       
    #     db.session.commit()
          

    #     return '<h1>DB Seeded!</h1>'
    # # Erase the Database (admins only)
    # @app.route('/erase_DB')
    # def eraseDB():
    #     meals = Meals.query.all()
    #     db.session.delete(meals)
    #     db.session.commit()
    #     return '<h1>DB Erased!</h1>'