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
});
