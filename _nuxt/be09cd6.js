(window.webpackJsonp=window.webpackJsonp||[]).push([[22],{326:function(t,e,r){"use strict";r.r(e);var n=r(7),o=(r(37),{asyncData:function(t){return Object(n.a)(regeneratorRuntime.mark((function e(){var r,n,o;return regeneratorRuntime.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return r=t.$content,n=t.params,e.next=3,r("articles",n.slug).where({"author.name":{$regex:[n.author,"i"]}}).without("body").sortBy("createdAt","asc").fetch();case 3:return o=e.sent,e.abrupt("return",{articles:o});case 5:case"end":return e.stop()}}),e)})))()},methods:{formatDate:function(t){return new Date(t).toLocaleDateString("en",{year:"numeric",month:"long",day:"numeric"})}}}),c=r(18),component=Object(c.a)(o,(function(){var t=this,e=t.$createElement,r=t._self._c||e;return r("div",[r("h1",[t._v("Author: "+t._s(t.articles[0].author.name))]),t._v(" "),r("p",[t._v("Bio: "+t._s(t.articles[0].author.bio))]),t._v(" "),r("h3",[t._v("Here are a list of articles by "+t._s(t.articles[0].author.name)+":")]),t._v(" "),r("ul",t._l(t.articles,(function(article){return r("li",{key:article.slug},[r("NuxtLink",{attrs:{to:{name:"blog-slug",params:{slug:article.slug}}}},[r("img",{attrs:{src:article.img,alt:article.alt}}),t._v(" "),r("div",[r("h2",[t._v(t._s(article.title))]),t._v(" "),r("p",[t._v(t._s(article.description))]),t._v(" "),r("p",[t._v(t._s(t.formatDate(article.updatedAt)))])])])],1)})),0)])}),[],!1,null,null,null);e.default=component.exports}}]);