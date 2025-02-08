import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { Login } from "./screens/Login";
import { Home } from "./screens/Home";
import { Home1 } from "./screens/Home_1";
import { Home2 } from "./screens/Home_2";
import { Home3 } from "./screens/Home_3";
import { Home4 } from "./screens/Home_4";
import { Challenge } from "./screens/Challenge";
import { Library_home } from "./screens/Library_home";
import { Library_1 } from "./screens/Library_1";
import { Timer } from "./screens/Timer";
import { Community } from "./screens/Community";
import { Review } from "./screens/Review/review";

function App() {
  return (
    <Router>
      <Routes>
        {/* 기본 로그인 페이지 */}
        <Route path="/" element={<Login />} />

        {/* 네이버 로그인 성공 후 자동으로 Home 페이지 이동 */}
        <Route path="/Home" element={<Home />} />
        <Route path="/Home_1" element={<Home1 />} />
        <Route path="/Home_2" element={<Home2 />} />
        <Route path="/Home_3" element={<Home3 />} />
        <Route path="/Home_4" element={<Home4 />} />

        <Route path="/Challenge" element={<Challenge />} />

        <Route path="/Library" element={<Library_home />} />
        <Route path="/Library_detail" element={<Library_1 />} />

        <Route path="/Timer" element={<Timer />} />

        <Route path="/Commu" element={<Community />} />
        <Route path="/Review" element={<Review />} />
      </Routes>
    </Router>
  );
}

export default App;
