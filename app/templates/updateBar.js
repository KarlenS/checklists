var main = function() {

    $('body').scrollspy({ target: '#navtimes' });

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
        "positionClass": "toast-bottom-full-width",
        "preventDuplicates": false,
        "onclick": null,
        "showDuration": "300",
        "hideDuration": "1000",
        "timeOut": "2000",
        "extendedTimeOut": "1000",
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


    //toastr.error('FUCK?!');
  });
    $('#reset').click(function (){
      $("#progress-bar")
      .css("width", "0%")
      .attr("aria-valuenow", '0')
      .text("0/126");
    })
    
  $(':checkbox:checked').prop('checked',false);//this clears checkboxes on refresh
}

$(document).ready(main);
