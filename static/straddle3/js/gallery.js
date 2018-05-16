!(function($){
  $(document).ready( function(){
      $('#gallery-left-button').click( function(){
          var first = $('#gallery-container li:first-child')
          var last  = $('#gallery-container li:last-child');
          last.insertBefore(first);
      });
      $('#gallery-right-button').click( function(){
          var first = $('#gallery-container li:first-child')
          var last  = $('#gallery-container li:last-child');
          first.insertAfter(last);
      });
  });
})(jQuery);
