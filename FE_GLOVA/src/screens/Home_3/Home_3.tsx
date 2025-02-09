import { useEffect, useCallback, useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { Question2Server } from "../../api/api";
import NaviBar from "../../components/ui/navigationbar";
import { motion } from "framer-motion"; // 애니메이션을 위한 라이브러리

export const Home3 = (): JSX.Element => {
  const location = useLocation();
  const navigate = useNavigate();
  const { age, gender, question } = location.state || {};
  const [loading, setLoading] = useState(true);

  {/*더미 데이터*/}
  // const fetchAndNavigate = useCallback(async () => {
  //   try {   
  //     setLoading(true); // 로딩 상태 활성화
      
  //     await new Promise((resolve) => setTimeout(resolve, 5000)); // 5초 대기
  //     navigate("/Home_4");

  //   } catch (error) {
  //     console.error("Error while fetching data:", error);
  //   } finally {
  //     setLoading(false); // 로딩 상태 비활성화
  //   }
  // }, [age, gender, question, navigate]);

  {/*서버 통신 데이터*/}
  const fetchAndNavigate = useCallback(async () => {
    try {
      console.log(age, gender, question);
      const data = await Question2Server(age, gender, question);
      navigate("/Home_4", { state: { ...data } });
    } catch (error) {
      console.error("Error while fetching data:", error);
    } finally {
      setLoading(false);
    }
  }, [age, gender, question, navigate]);

  useEffect(() => {
    fetchAndNavigate();
  }, [fetchAndNavigate]);

  return (
    <div className="bg-gray-500 flex flex-row justify-center w-full">
      <div className="bg-white w-[393px] min-h-screen relative flex flex-col">
        {/* 로딩 메시지 */}
        <div className="absolute top-[180px] left-16 font-bold text-black text-base text-center">
          무슨 책을 추천할지 고민 중입니다...
        </div>

        {/* 점 애니메이션 */}
        <div className="inline-flex top-[125px] left-[165px] items-center gap-[15px] absolute">
          <motion.div
            className="w-2.5 h-2.5 bg-[#b38f00] rounded-[5px]"
            animate={{ scale: [1, 1.5, 1] }}
            transition={{ duration: 1, repeat: Infinity, ease: "easeInOut" }}
          />
          <motion.div
            className="w-2.5 h-2.5 bg-[#b38f00] rounded-[5px]"
            animate={{ scale: [1, 1.5, 1] }}
            transition={{ duration: 1, repeat: Infinity, ease: "easeInOut", delay: 0.2 }}
          />
          <motion.div
            className="w-[13px] h-[13px] bg-[#ffcc00] rounded-[6.5px]"
            animate={{ scale: [1, 1.5, 1] }}
            transition={{ duration: 1, repeat: Infinity, ease: "easeInOut", delay: 0.4 }}
          />
        </div>

        {/* 로딩 이미지 */}
        <div className="absolute w-[351px] top-[220px] left-[21px] flex justify-center">
          {loading ? (
            <motion.img
              src="../../image_data/P0i7.gif" // 로딩 이미지 추가
              alt="Loading..."
              className="w-[300px] h-[300px]"
              transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
            />
          ) : null}
        </div>

        <NaviBar activeLabel="Home" />
      </div>
    </div>
  );
};
