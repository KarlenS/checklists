var main = function() {

    $('body').scrollspy({ target: '#navtimes' });

/*
    var getMessage = function (i) {
    var msgs = ['Another one!',
                'You smart.',
                'You very smart!',
                'We da best!',
                'You a genius!',
                'I appreciate you.',
                'You loyal.',
                'I changed ALOT. You can too :)',
                'WIN WIN WIN no matter what!',
                'Never give up, never surrender.',
                'Put this money in your savings account.',
                'Buy yo mama a house.',
                'Buy your whole family houses.',
                'Another one!',
                'Another one!',
                'Another one!',
            ];

            return msgs[i];
        };

    $('input').on('click', function(){

        toastr.options = {
        "closeButton": false,
        "debug": false,
        "newestOnTop": false,
        "progressBar": false,
        "positionClass": "toast-top-right",
        "preventDuplicates": false,
        "onclick": null,
        "showDuration": "1000",
        "hideDuration": "2000",
        "timeOut": "3000",
        "extendedTimeOut": "2000",
        "showEasing": "swing",
        "hideEasing": "linear",
        "showMethod": "fadeIn",
        "hideMethod": "fadeOut"
        }   

    if(this.checked){
      var i = Math.floor((Math.random() * 15));
      var msg = getMessage(i);
      toastr.success(msg);
       
    }
    else {
      toastr.error('NOOOOOOOOOO!');
    }
    //if(value == 126) 

  });
*/
    $('#reset').click(function (){
      $("#progress-bar")
      .css("width", "0%")
      .attr("aria-valuenow", '0')
      .text("0%");
    })
}

$(document).ready(main);
