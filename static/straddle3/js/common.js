/**
 * common.js
 * Common scripts to be used throughout the site
 */


 /**
 *  Add event listeners when DOM is completely loaded
 *  equivalent to $(document).ready()
 */
document.addEventListener("DOMContentLoaded", function()
{
    var w = Math.max(document.documentElement.clientWidth, window.innerWidth || 0);
    var mobile = w < 740;

    var seemore_button = document.querySelector('.see-more');
    var body = document.querySelector('body');
    if(seemore_button){
        body.classList.add('trimmed-content');
        seemore_button.addEventListener('click', function(){
            body.classList.remove('trimmed-content');
        });
        document.querySelector('.see-less').addEventListener('click', function(){
            body.classList.add('trimmed-content');
        })
    }

    var lastScrollTop = 0;
    if(!mobile){
        window.addEventListener('scroll', function(){
            var header = document.querySelector('.region-header');
            var st = window.pageYOffset || document.documentElement.scrollTop;
            if (st > lastScrollTop){
                if(!header.classList.contains('hidden')){
                    header.classList.add('hidden');
                    header.classList.remove('visible');
                }
            } else {
                if(header.classList.contains('hidden')){
                    header.classList.remove('hidden');
                    header.classList.add('visible');
                }
            }
            lastScrollTop = st <= 0 ? 0 : st;
        }, false);
    }
    var menu_launcher = document.querySelector('.menu-main__launcher');
    menu_launcher.addEventListener('click', function(){
      window.scrollTo(0, 0);
        document.body.classList.toggle('navigation-open');
    });

    var search_query   = document.querySelector('.search-widget__query');
    search_query.value = '';
    document.querySelector('.collapsed .search-widget__submit').addEventListener('click', function(e){
        if( !search_query.value ){
            e.preventDefault();
            document.querySelector('.search-widget').classList.toggle('collapsed');
        }
    });
});
