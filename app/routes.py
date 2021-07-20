from flask import render_template, flash, redirect, url_for, request
import requests
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, EditParameters
from app.models import User
import keys as k
from bs4 import BeautifulSoup
from  mws import mws
import time
import os




@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('search'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('search')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/settings', methods=['GET'])
@login_required
def dropdown():
    return render_template('settings.html')

@app.route('/privacy')
def privacy():
    return render_template('Privacy.html')

@app.route('/settings/parameters', methods=['GET','POST'])
@login_required
def parameters():
	form = EditParameters()
	if form.validate_on_submit():
		current_user.rank1 = form.rank1.data
		current_user.rank2 = form.rank2.data
		current_user.rank3 = form.rank3.data
		current_user.rank4 = form.rank4.data
		current_user.rank5 = form.rank5.data
		current_user.price1 = form.price1.data
		current_user.price2 = form.price2.data
		current_user.price3 = form.price3.data
		current_user.price4 = form.price4.data
		current_user.price5 = form.price5.data		
		db.session.commit()
		flash('Your changes have been saved.')
		return redirect(url_for('parameters'))
	elif request.method == 'GET':
		form.rank1.data = current_user.rank1
		form.price1.data = current_user.price1
		form.rank2.data = current_user.rank2
		form.price2.data = current_user.price2
		form.rank3.data = current_user.rank3
		form.price3.data = current_user.price3
		form.rank4.data = current_user.rank4
		form.price4.data = current_user.price4
		form.rank5.data = current_user.rank5
		form.price5.data = current_user.price5
	return render_template('parameters.html', title='parameters',form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@app.route('/search')
@login_required
def post():
    return render_template('search.html')

products_api = mws.Products(k.access_key, k.secret_key, k.seller_id, region='US')
@app.route("/", methods=['POST'])
@app.route('/search', methods=['POST'])
@login_required
def search():
	start = time.time()
	query = request.form['text']
	products = products_api.list_matching_products(marketplaceid=k.marketplace_usa, query=query)
	productsxml = products.original
	xml= mws.remove_namespace(productsxml)
	soup1 = BeautifulSoup(xml, 'lxml')
	a = soup1.asin.string
	b = [a]
	offers = products_api.get_lowest_offer_listings_for_asin(marketplaceid=k.marketplace_usa, asins=b, condition="Used", excludeme="False")
	offersxml = offers.original
	xml= mws.remove_namespace(offersxml)
	soup2 = BeautifulSoup(xml, 'lxml')
	condition = soup2.find_all('itemsubcondition')[0:3]
	prices1 = soup2.find_all('price')[0:3]
	
	parameters = {'key': k.access_id, 'q': query}
	r = requests.get("https://www.goodreads.com/search/index.xml", 			params=parameters)	
	soup3 = BeautifulSoup(r.content, 'lxml')
	class data:
		def __init__(self):
			conditions = []
			prices=[]		
			for cond in condition:
				conditions.append(cond.string)
			for pr in prices1:
				price_wship = pr.listingprice.amount.string + " + " + pr.shipping.amount.string
				prices.append(price_wship)
			self.title = soup1.title.string
			self.rank = soup1.rank.string
			self.asin = soup1.asin.string
			self.binding = soup1.binding.string
			self.cprice = soup2.listingprice.amount.string			
			self.price = prices[0]
			self.price2 = prices[1]
			self.price3 = prices[2]
			self.shape = conditions[0]
			self.shape2 = conditions[1]
			self.shape3 = conditions[2]	
			self.image = soup3.image_url.string
			rank_val = float(soup1.rank.string)
			price_val = float(soup2.price.listingprice.amount.string)
			self.sound = 1
			self.audio = 0
			self.buy = "BUY!"
			if rank_val < current_user.rank1 and price_val > current_user.price1:	
				pass							
			elif rank_val < current_user.rank2 and price_val > current_user.price2:	
				pass
			elif rank_val < current_user.rank3 and price_val > current_user.price3:	
				pass
			elif rank_val < current_user.rank4 and price_val > current_user.price4:	
				pass
			elif rank_val < current_user.rank5 and price_val > current_user.price5:	
				pass
			else:
				self.sound = "0"
				self.buy = " "

			if self.sound ==1:
				self.audio = 'http://www.soundjay.com/appliances/sounds/microwave-oven-bell-1.mp3'
			else:
				pass	
			end = time.time()			
			time1 = end - start
			self.time1 = str(time1)[:4]
			
	def val():
		return data()
	val = val()

	return render_template('search.html', sound=val.audio, time1= val.time1,title=val.title,binding=val.binding,rank=val.rank, price=val.price,price2 = val.price2, price3=val.price3,shape=val.shape, shape2=val.shape2,shape3=val.shape3, image=val.image, buy=val.buy)

@app.errorhandler(500)
def page_not_found(e):
	return render_template("search.html")