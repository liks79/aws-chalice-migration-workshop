        function getReverseGeocodingData(lat, lng, exif_flag) {
            var latlng = new google.maps.LatLng(lat, lng);
            // This is making the Geocode request
            var geocoder = new google.maps.Geocoder();
            geocoder.geocode({ 'latLng': latlng }, function (results, status) {
                if (status !== google.maps.GeocoderStatus.OK) {
                    msgbox(status);
                }
                // This is checking to see if the Geoeode Status is OK before proceeding
                if (status == google.maps.GeocoderStatus.OK) {

                    console.log(results);
                    addr_comp_length=results[0].address_components.length;

                    if(addr_comp_length == 8) {
                        var city = results[0].address_components[2].long_name;
                        var nation = results[0].address_components[6].long_name;
                        var address = results[0].formatted_address;
                    }

                    if(addr_comp_length == 7) {
                        var city = results[0].address_components[2].long_name;
                        var nation = results[0].address_components[5].long_name;
                        var address = results[0].formatted_address;
                    }

                    if(addr_comp_length == 6) {
                        var city = results[0].address_components[3].long_name;
                        var nation = results[0].address_components[4].long_name;
                        var address = results[0].formatted_address;
                    }
                    $('[name=lat]').val(lat);
                    $('[name=lng]').val(lng);
                    $('[name=city]').val(city);
                    $('[name=nation]').val(nation);
                    $('[name=formatted_address]').val(address);
                    $('[name=address]').val(address);

                    if(exif_flag == true) {
                        $("#exif-info").append("<span class=\"badge badge-secondary\">"+city+" <\/span> "+
                                "<span class=\"badge badge-secondary\">"+nation+" <\/span> " +
                                "<span class=\"badge badge-secondary\">"+address+" <\/span> "
                        );
                    }

                    $("#address-info").html("<span class=\"badge badge-info\">"+address+" <\/span> ");

                }
            });
        }


        // 지도에서 마우스클릭으로 사용자가 원하는 위치를 직접 입력 가능하도록 해주는 함수
        GMaps.on('click', map.map, function(event) {
            var index = map.markers.length;
            var lat = event.latLng.lat();
            var lng = event.latLng.lng();

            // 최종 위치만 필요함으로 이미 설정된 모든 marker를 제거한다.
            map.removeMarkers();

            map.addMarker({
                lat: lat,
                lng: lng,
            });

            // 최종 위치정보 업데이트
            $('[name=lat]').val(lat);
            $('[name=lng]').val(lng);
            getReverseGeocodingData($('[name=lat]').val(), $('[name=lng]').val(), false);

        });


        // Set current location information
        function currentLocation() {
            GMaps.geolocate({
                success: function(position) {
                    map.setCenter(position.coords.latitude, position.coords.longitude);
                    // 최종 위치만 필요함으로 이미 설정된 모든 marker를 제거한다.
                    map.removeMarkers();

                    map.addMarker({
                        lat: position.coords.latitude,
                        lng: position.coords.longitude
                    });

                    // 최종 위치정보 업데이트
                    $('[name=lat]').val(position.coords.latitude);
                    $('[name=lng]').val(position.coords.longitude);
                },

                error: function(error) {
                    msgbox('Geo-location failed : ' + error.message);
                },

                not_supported: function() {
                    msgbox("Your browser does not support geo-location.");
                },

                always: function() {
                    getReverseGeocodingData($('[name=lat]').val(), $('[name=lng]').val(), false);
                    msgAlert("Your location information is being updated..");
                }
            });
        }


        function gmapSearch() {
            if($('#address').val().trim() == "") {
                msgbox('Enter where you took the photo.');
                $('#address').focus();
                return false;
            }

            // 입력된 위치를 검색하여 위치를 보여준다
            GMaps.geocode({
                address: $('#address').val().trim(),
                callback: function(results, status){
                    if(status=='OK'){
                        var latlng = results[0].geometry.location;
                        map.setCenter(latlng.lat(), latlng.lng());

                        // 최종 위치만 필요함으로 이미 설정된 모든 marker를 제거한다.
                        map.removeMarkers();
                        // 최종 위치 마킹
                        map.addMarker({
                            lat: latlng.lat(),
                            lng: latlng.lng()
                        });

                        // 최종 위치정보 업데이트
                        $('[name=lat]').val(latlng.lat());
                        $('[name=lng]').val(latlng.lng());

                    }
                }
            });
        }
		
		
		
		
        // Exif정보를 파싱후 ConvertDMSToDD 로 전달하여 decimal 값을 리턴한다.
        function toDecimal(gps_src, gps_ref){

            var temp_array="";
            temp_array = gps_src.toString();
            temp_array = temp_array.split(",");

            deg = temp_array[0];
            min = temp_array[1];
            sec = temp_array[2];
            ref = gps_ref;

            return ConvertDMSToDD(deg, min, sec, ref);
        }


        // Exif에서 읽어온 GPS정보를 decimal 값으로 변환하는 함수
        function ConvertDMSToDD(degree, minutes, seconds, direction) {

            var dd = parseFloat(degree) + parseFloat(minutes/60) + parseFloat(seconds/(60*60));

            if (direction == "S" || direction == "W") {
                dd = dd * -1;
            } // Don't do anything for N or E

            return dd;
        }
		

        function no_exif() {
            var reader = new FileReader();
            var file = photo.files[0];
            reader.readAsDataURL(file);
            reader.onload = function (e) {

                var image = new Image();
                image.src = e.target.result;
                image.onload = function () {
                    var taken_date = new moment(file.lastModified).format("YYYY:MM:DD HH:mm:ss");
                    $('[name=height]').val(this.height);
                    $('[name=width]').val(this.width);
                    $('[name=taken_date]').val(taken_date);
                    $("#exif-info").html("<span class=\"badge badge-warning\"><i class=\"fas fa-exclamation-triangle\"></i> No EXIF"+" <\/span> "+
                            "<span class=\"badge badge-secondary\">"+taken_date+" <\/span> "+
                            "<span class=\"badge badge-secondary\">"+this.width+" x "+this.height+"<\/span> "
                    );
                    $('[name=make]').val('');
                    $('[name=model]').val('');

                    getReverseGeocodingData(initial_lat, initial_lng, false);

                    //$('[name=city]').val('');
                    //$('[name=nation]').val('');
                    //$('[name=address]').val('');
                }
            }
        }



        // 사진 업로드를 위해 사용자가 로컬에서 사진을 선택하여
		// 'photo' ID셀렉터에 'change'이벤트가 발생하면 구동되는 함수
		// 사진의 미리보기를 만들고, exif 정보를 추출한다.
		$("#photo").change(function() {

		    //clear();

		    var file = this.files[0];
		    fr   = new FileReader;
           
            $('[name=filename_origin]').val(this.files[0].name);
            console.log('filename:'+$('[name=filename_origin]').val());

		    fr.onloadend = function() {

                // Reference code : http://jsfiddle.net/xQnMd/1/
		        var exif = EXIF.readFromBinaryFile(new BinaryFile(this.result));

                // exif에서 GPS정보를 가져올 수 없는 경우
                if(exif.GPSLatitude == undefined) {
                   msgAlert('EXIF metadata \<strong\>not found!\<\/strong\> Please set up location information.');
                   $('#exif-info').html('');
                   no_exif();
                }

                // exif에서 GPS정보를 가져올 수 있는 경우
                else {

                    // 사진파일의 exif를 이용하여 해당 값들을 설정함
                    $('[name=taken_date]').val(exif.DateTimeOriginal);
                    $('[name=lat]').val(toDecimal(exif.GPSLatitude, exif.GPSLatitudeRef));
                    $('[name=lng]').val(toDecimal(exif.GPSLongitude, exif.GPSLongitudeRef));
                    $('[name=make]').val(exif.Make);
                    $('[name=model]').val(exif.Model);
                    $('[name=width]').val(exif.PixelXDimension);
                    $('[name=height]').val(exif.PixelYDimension);

                    // 최종 위치만 필요함으로 이미 설정된 모든 marker를 제거한다.
                    map.removeMarkers();
                                            // 위치정보 업데이트
                    map.setCenter($('[name=lat]').val(), $('[name=lng]').val())
                    map.addMarker({
                        lat: $('[name=lat]').val(),
                        lng: $('[name=lng]').val()
                    });

                    $("#exif-info").html("<span class=\"badge badge-info\"><i class=\"fas fa-camera\"></i> EXIF<\/span> "+
                                         "<span class=\"badge badge-secondary\">"+exif.DateTimeOriginal+" <\/span> "+
                                         "<span class=\"badge badge-secondary\">"+exif.Make+" <\/span> "+
                                         "<span class=\"badge badge-secondary\">"+exif.Model+" <\/span> "+
                                         "<span class=\"badge badge-secondary\">"+exif.PixelXDimension+" x "+exif.PixelYDimension+" <\/span> "
                    );

                    getReverseGeocodingData($('[name=lat]').val(), $('[name=lng]').val(), true);
                    msgAlert("EXIF metadata found!");
                }
		    };

		    try {
		        fr.readAsBinaryString(file);
            }
            catch (e) {
		        console.log("Image file removed from upload form!");
            }
		});


