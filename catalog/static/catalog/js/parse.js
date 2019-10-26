$(document).ready(function(){
//    console.log('span event handler linked')
    $("span").click(function(){
        $(this).toggleClass('highlighted_lemma')
    })
})