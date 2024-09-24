---
layout: post
title:  CabanaPIC
category: app
categories: [Particle-in-Cell,Structured Grid,Mini-Application]
---
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20,400,0,0" />
<a href="{{ site.baseurl }}{% link explore.html %}">Back</a>
<h1>CabanaPIC</h1>
<br>
A mini-PIC (particle-in-cell) code based on the Cabana library, which is developed in the ECP COPA project. The algorithm employed in the code is standard explicit PIC in Cartesian geometry solving relativistic Vlasov-Maxwell equations.


<div class="container">
{% for post in site.posts %}
{% if post.categories contains "CabanaPIC" %}
<div class="filterDiv">
<div class="filterHeader">
<a href="{{ site.baseurl }}{{ post.url }}" style="text-decoration: none;font-size: large;">
{{ post.title }}
</a>
</div>    
<div class="contentContainer">
{% capture tags %}
{%- for tag in post.tags -%}
{{ tag | append: ',' }}
{%- endfor -%}
{% endcapture %}
{% assign length = tags | size | minus: 1 %}
{% assign outputString = tags | truncate: length, "" %}
<p style="display: inline-block;margin:0px;"><span class="material-symbols-outlined">
sell</span>{{ outputString | upcase }}</p>
</div>
</div>
{% endif %}
{% endfor %}
</div>


<style>
.container {
overflow: hidden;
align-items: start;
text-align: left;
height: 100%;
}
.filterDiv{
border: 1px solid #ccc;
border-radius: 2px;
min-height: 62px;
height: fit-content;
text-align: center;
margin: 5px;
display: inline-block;
width: 99%;
}
.filterHeader{
border: 1px solid #ccc;
background-color: #ccc;
min-height: 30px;
height: fit-content;
font-size: large;
width: 100%;
}
.contentContainer{
position:relative;
text-align: center;
top:0px; 
font-size:medium; 
line-height: 23px;
padding-left: 2px;
padding-right: 2px;
padding-top: 2px;
padding-bottom: 0px;
min-height: 32px;
height: fit-content;
overflow: hidden;
text-overflow: ellipsis;
width: 100%;
}
</style>
<h3>Sources:</h3>[GitHub](https://github.com/ECP-copa/CabanaPIC)<br>