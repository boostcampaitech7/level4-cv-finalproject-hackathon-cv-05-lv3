import {
    BookOpen,
    HomeIcon,
    TimerIcon,
    TrophyIcon,
  } from "lucide-react";
  
import { Vector } from "../../icons/Vector";  
import { Button } from "../../components/ui/button";
import { Card, CardContent } from "../../components/ui/card";
import { BrowserRouter as Router, Route, Routes, useNavigate, useLocation } from "react-router-dom";
import { Calendar2Server } from "../../api/api";
import { useEffect } from "react";

const navigationItems = [
  { icon: TrophyIcon, label: "CHALLENGE", href: "/Challenge", active: false },
  { icon: HomeIcon, label: "HOME", href: "/Home", active: true },
  { icon: BookOpen  , label: "BOOKS", href: "/Library", active: false },
  { icon: TimerIcon, label: "TIMER", href: "/Timer", active: false },
];

export const Map = (): JSX.Element => {
  const location = useLocation();
  const navigate = useNavigate();
  
  const data = location.state || {};

  useEffect(() => {
    const clientId = import.meta.env.VITE_MAP_CLIENT_ID;

    if (!clientId) {
      console.error("네이버 지도 API 클라이언트 ID가 설정되지 않았습니다.");
      return;
    }
    const script = document.createElement("script");
    script.src = `https://oapi.map.naver.com/openapi/v3/maps.js?ncpClientId=${clientId}`;
    script.async = true;
    script.onload = () => {
      const { naver } = window as any;
  
      if (!naver) {
        console.error("Naver Maps API failed to load.");
        return;
      }
  
      const map = new naver.maps.Map("map", {
        center: new naver.maps.LatLng(37.5666805, 126.9784147),
        zoom: 13,
        mapTypeId: naver.maps.MapTypeId.NORMAL,
      });
  
      const infowindow = new naver.maps.InfoWindow();
  
      function onSuccessGeolocation(position: GeolocationPosition) {
        const location = new naver.maps.LatLng(
          position.coords.latitude,
          position.coords.longitude
        );
  
        map.setCenter(location);
        map.setZoom(13);
  
        infowindow.setContent(
          '<div style="padding:20px;">geolocation.getCurrentPosition() 위치</div>'
        );
        // infowindow.open(map, location);
        console.log("Coordinates: " + location.toString());

        // 위치 마커 추가
        new naver.maps.Marker({
          position: location,
          map: map
        });
      }
  
      function onErrorGeolocation() {
        const center = map.getCenter();
        infowindow.setContent(
          `<div style="padding:20px;">
            <h5 style="margin-bottom:5px;color:#f00;">Geolocation failed!</h5>
            latitude: ${center.lat()}<br />longitude: ${center.lng()}
          </div>`
        );
        infowindow.open(map, center);
      }
  
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(onSuccessGeolocation, onErrorGeolocation);
      } else {
        const center = map.getCenter();
        infowindow.setContent(
          '<div style="padding:20px;"><h5 style="margin-bottom:5px;color:#f00;">Geolocation not supported</h5></div>'
        );
        infowindow.open(map, center);
      }
    };
    document.body.appendChild(script);
  }, []);  

  return (
    <div className="flex justify-center w-full bg-white">
      <div className="relative w-[393px] h-[852px] bg-white">
        {/* Top Bar */}
        <Vector className="!absolute !w-9 !h-6 !top-[30px] !left-[332px]" />

        {/* Main Content */}
        <div className="flex flex-col items-center px-4">
          {/* Naver Map Container */}
          <div id="map" className="w-[325px] h-[200px] mt-4 border rounded-md"></div>
        </div>
      </div>
    </div>
  );
};
