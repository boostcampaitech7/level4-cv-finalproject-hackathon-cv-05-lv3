import { Button } from "../../components/ui/button";
import { Card, CardContent } from "../../components/ui/card";

export const Login = (): JSX.Element => {
  // 네이버 로그인 버튼 클릭 시 OAuth 요청
  const handleNaverLogin = () => {
    window.location.href = "http://127.0.0.1:8000/login/naver";
  };

  return (
    <main className="flex justify-center items-center min-h-screen bg-whit">
     <div className="w-[393px] flex flex-col items-center px-4 bg-white">
        {/* <img className="w-[250px] h-[148px] mb-4 object-cover" alt="Logo" src="./image_data/rectangle-4@2x.png" /> */}
        <p className="text-[40px] text-center text-green-500 font-SBAggroB">
          Hi Book
        </p>
        <p className="text-[60px] text-center text-black font-SBAggroB mb-5">
          GLOVA
        </p>

        <p className="text-xl text-center text-black font-SBAggroB mb-12">
          함께 읽어가는 우리들의 챌린지
        </p>

        <Card className="w-full bg-transparent border-none shadow-none">
          <CardContent className="flex flex-col gap-4 items-center">
            <Button onClick={handleNaverLogin} className="px-4 py-2 bg-green-500 text-white rounded active:scale-95 transition-transform duration-150 hover:bg-green-600">
              네이버 로그인
            </Button>
          </CardContent>
        </Card>
      </div>
    </main>
  );
};
