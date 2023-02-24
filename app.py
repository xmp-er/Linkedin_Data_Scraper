from flask import Flask,render_template,request,jsonify
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
app = Flask(__name__)

@app.route('/',methods=['POST','GET'])
def m():
    return render_template('index.html')

@app.route('/review',methods=['POST'])
def company_results():
    if request.method=='POST':
        post_query=request.form['post_query']
        base_url='https://www.reddit.com/search/?q='
        post_search_url=base_url+post_query
        #check if no results
        post_search_page=urlopen(post_search_url)
        post_search_page = bs(post_search_page, 'html.parser')
        divs_containing_posts=post_search_page.findAll('div',{'class':'_2dkUkgRYbhbpU_2O2Wc5am'})
        res=""
        reviews = []
        if(len(divs_containing_posts)==0):
            res+="No posts"
        else:
            for i in range(len(divs_containing_posts)):
                title_of_the_current_post=divs_containing_posts[i].find('div',{'class':'_1AKeAGcglmBjK1SUUXNFti _1-SZ3VwLjbFwTzaZvU8FBX _1FT0e6kh1BBb_oALAMW_l7 _1yBpz1MEPxxYTxjlEilGtB'}).h3.text
                #checking if the post has comments or not
                #the 1st element of the bar denotes the comments
                comments_of_current_post=divs_containing_posts[i].findAll('span',{'class':'_vaFo96phV6L5Hltvwcox'})[1].text
                final_comments=''
                if(comments_of_current_post=='0 comments'):
                    final_comments='No comments'
                else:
                    post_page=divs_containing_posts[i].div.div.find('div',{'class':'_2n04GrCyhhQf-Kshn7akmH _19FzInkloQSdrf0rh3Omen'})
                    post_page=post_page.div.div.a['href']
                    post_link='https://www.reddit.com/'+post_page
                    post_upvotes=divs_containing_posts[i].findAll('span',{'class':'_vaFo96phV6L5Hltvwcox'})[0].text
                    final_comments=divs_containing_posts[i].findAll('span',{'class':'_vaFo96phV6L5Hltvwcox'})[1].text
                mydict = {"Title":title_of_the_current_post, "Comment":comments_of_current_post, "Upvotes": post_upvotes, "Link": post_link}
                reviews.append(mydict)
        return render_template('result.html', reviews=reviews[0:(len(reviews)-1)])

if __name__=="__main__":
    app.run(host="0.0.0.0")
