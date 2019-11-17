// $(document).ready(function(){
// //    console.log('span event handler linked')
//     $("span").click(function(){
//         console.log($(this).attr("id"))
//         $("span#" + $(this).attr("id")).toggleClass('highlighted_lemma')
//     })    
// })

var app = new Vue({
    el: '#parsed_book',
    data: {
        opacity: {}
    },
    methods: {
        add: function(event){
            var el = event.currentTarget
            // el.className = 'highlight'
            var elementId = el.id
            if (elementId in this.opacity) {
                if (this.opacity[elementId] >=1) {
                    this.opacity[elementId] = 1
                } else
                {
                    this.opacity[elementId] += 0.1
                }
            } else {
                this.opacity[elementId] = 0.1
            }
            console.log(elementId)
            console.log(this.opacity[elementId])
        }
    },
    computed: {
        
    },
    // mounted(){
    //     lemmas = document.body.getElementById(‘id’)
    //     console.log(this)
    //     // console.log(this.$root.$children.find(child => { return child.$options.name === "name"; }))
    // }
})
