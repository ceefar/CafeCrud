# CafeCrud   
Very first data engineering bootcamp project (solo) - CRUD Cafe App  
  
#### Key Features  
- **Pagination**  
- **Upsell/Scarcity Functionality**  
- **Multiple Modules**  
- **Full Crud**  
- **Multiple File Types**  
- **Class Based Structure**  
- **Secure Login**  
- **External Packages**
- **Discord Bot** 
  
#### Overview  
**Pagination**  
My most proud implemented feature, included complex mathematics using arrays for dynamic pagination  
Truly dynamic with spacing by string length, plus using user set columns and page/terminal height, and dynamic user set sorting options e.g. sort by price  
Had further plans to expand and clean this up but unfortunately had emergency surgery 3 days before hand in (see notes at the bottom of the readme)  
Check out the images to see it in action, note the output order is vertical despite print being performed horizontally  
  
**Pagination Example Images**    
Default Pagination - note scarcity display, current page highlight, dynamic spacing applied by string length, etc  
<img src="https://thehardgainerbible.com/wp-content/uploads/2022/08/pagination1.png" alt="ProductsPagination1" width="500"/>
<img src="https://thehardgainerbible.com/wp-content/uploads/2022/08/pagination2.png" alt="ProductsPagination2" width="500"/>  
  
Dynamic Pagination Based On User Inputs :heart_eyes:  
Updated with user inputs to tall height with 2 columns (instead of the default 3 col), all implemented dynamically    
<img src="https://thehardgainerbible.com/wp-content/uploads/2022/07/CafeCrud_ProductsPagination_DynamicExample_TallPageOneColumn.png" alt="DynamicPagination" width="500"/>

   
**Multiple Modules**  
Orders -  In depth ordering system with delivery charge, and on the fly product quantity db updating  
Couriers - Assign couriers to orders for delivery with order status avilability for each courier (i.e. "2 orders out for delivery"   
Products - In depth product catalogue with stock tracking, pricing, scarcity, dynamic displays  
Full CRUD - All modules upload to local db, full crud queries for each using MySQL (create, read/print, update, delete)  
  
**Secure Login**  
Hashed, salted, and peppered passwords stored securely in database + passed rainbow table tests on md5decrypt.net/   

**Upsell/Scarcity Functionality**  
Upsell prompt user to purchase more items if under a delivery threshold  
Scarcity prompt highlights items low in stock  

**File Handling**  
Initial simple local file save/load, from .txt then to -> .csv then to -> .json  
Next with class implementation, class objects were stored using -> .pickle  
Finally spinning up local mysql db allowed for local hosting of data in database (full crud queries)  

**External Packages**  
PyInquirer - dynamic terminal menu system  
Colorama - because everything looks better in colour  

**Discord Bot**
Alpha - discord bot collected live db data and displayed images of products, didn't get to finish due to surgery mentioned in notes below  


#### Notes  
Please note 3 days before the project hand-in + presentation day I was admitted to A&E and had to have emergency surgery (appendicitis)  
Meaning I didn't have time to go back over the project for polish, or to finish off some tidbits and final functionalities (i.e. orders module may error due to this)  
This is primarily why the code isn't clean (pep8), but also because most of my time was spent experimenting as this literally was my very first project   

[![list-repo](https://github.com/ceefar/PyTest1/actions/workflows/example-action.yml/badge.svg)](https://github.com/ceefar/PyTest1/actions/workflows/example-action.yml)
