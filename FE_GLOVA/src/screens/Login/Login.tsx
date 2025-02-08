import { Button } from "../../components/ui/button";
import { Card, CardContent } from "../../components/ui/card";

export const Login = (): JSX.Element => {
  // 네이버 로그인 버튼 클릭 시 OAuth 요청
  const handleNaverLogin = () => {
    window.location.href = "http://127.0.0.1:8000/login/naver";
  };

  return (
    <main className="flex justify-center items-center min-h-screen bg-white">
      <div className="w-[393px] flex flex-col items-center px-4">
        <img className="w-[250px] h-[148px] mb-4 object-cover" alt="Logo" src="./image_data/rectangle-4@2x.png" />
        <p className="text-xl text-center text-black font-normal mb-8">
          오늘은 또 무슨 일이 생길까?
        </p>

        <Card className="w-full bg-transparent border-none shadow-none">
          <CardContent className="flex flex-col gap-4 items-center">
            <Button onClick={handleNaverLogin} className="px-4 py-2 bg-green-500 text-white rounded">
              네이버 로그인
            </Button>
          </CardContent>
        </Card>
      </div>
    </main>
  );
};
