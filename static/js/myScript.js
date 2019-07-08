// $(document).ready(function(){
//     $('#myConstructionModal').modal('show');
// }); 
 
$(document).ready(function(){
    bsCustomFileInput.init()
});


$(document).on("click",".open-galleryImg",function(){
    var img=$(this).find("img")
    var img_src=img.attr("src")
    $(".myImgbody #imgId").attr("src",img_src)
    
    $('#imagedisplay').modal('.show')
});

// window.setTimeout(function() {
//     $(".alert").alert('close');
  
// }, 4000);



$(document).ready(function(){
    $("#agree-check").click(function(){
        if ($(this).prop("checked")==true){
            $("#reg-but").prop('disabled',false)
            
        }
        if($(this).prop("checked") == false){
                
             $("#reg-but").prop('disabled',true)
        }
    })
});


$(document).ready(function(){
    $("#intern-check").click(function(){
        if($(this).prop("checked")==true){
            $("#intern-submit").prop("disabled",false)
        }
        if($(this).prop("checked") == false){
            $("#intern-submit").prop("disabled",true)
        }
    })
})


// $(document).ready(function(){

//     $('#activate').click(function(){
        
//         $('#vacancy-indicator').prop('checked',true);
        
//     });

//     $("#deactivate").click(function(){
//         $("#vacancy-indicator").prop("checked",false);
        
//     });
// });



// $(document).ready(function(){
//       var date_input=$('input[name="date"]'); //our date input has the name "date"
//       var container=$('.bootstrap-iso form').length>0 ? $('.bootstrap-iso form').parent() : "body";
//       var options={
//         format: 'mm/dd/yyyy',
//         container: container,
//         todayHighlight: true,
//         autoclose: true,
//       };
//       date_input.datepicker(options);
// });

 

jQuery(document).ready(function(){
    //$(".loading").delay(10000).hide(0);
    /*setTimeout(function(){
        $(".loading").hide(400);
    },3000); */
});



jQuery(document).ready(function() {
    
    $('.counter').counterUp();
    
});



$(document).ready(function(){
    
    $(window).scroll(function(){
        scroll_pos=$(window).scrollTop();
        if(scroll_pos > 350)
        {
            $("#custom-nav").css("background-color","#111120");
            $("#custom-nav").css("transition","0.5s");
            $("#custom-nav a").css("color","#fff");
            $("#cus-hamburger-icon").css("color","#fff");
            $(".dropdown-menu a").css("color","black");
            $(".dropdown-menu").css("background-color","rgba(255,255,255,0.8)");
            $(".datepicker-dropdown").css("background-color","white");

            $(".dropdown-menu a").hover(function(){
                $(this).css("color","black");
            });
            
        }else{
            $("#custom-nav").css("transition","0.5s");
            $("#custom-nav").css('background-color','#fff');
            $("#custom-nav a").css("color","black");
            $("#cus-hamburger-icon").css("color","#111120");
            $(".dropdown-menu a").css("color","white");
            $(".dropdown-menu").css("background-color","rgba(0,0,0,0.3)");
            $(".datepicker-dropdown").css("background-color","white");
            $(".dropdown-menu a").hover(function(){
                $(this).css("color","black");
            },function(){
                $(this).css("color","white");
            });
             
        }
    });
});



var modal=document.getElementById('id01');

window.onclick = function(event){
    if(event.target==modal){
        modal.style.display="none";
    }
}

/*function initMap() {
    // The location of Uluru
    var office = {lat: 26.70000000 , lng: 94.11361111};
    // The map, centered at Uluru
    var map = new google.maps.Map(
        document.getElementById('map'), {zoom: 4, center: office});
    // The marker, positioned at Uluru
    var marker = new google.maps.Marker({position: office, map: map});
  }*/
