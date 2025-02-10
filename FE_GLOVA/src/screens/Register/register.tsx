import { useState } from "react";
import { DuplicateCheck, SaveUserdata } from "../../api/api"; // API 호출 함수 가져오기

const Input = ({ type, value, onChange, required }) => (
  <input
    type={type}
    value={value}
    onChange={onChange}
    required={required}
    className="w-full p-2 border border-gray-300 rounded"
  />
);

const Label = ({ children }) => <label className="block font-medium mb-1">{children}</label>;

const Select = ({ value, onChange, options }) => (
  <select
    value={value}
    onChange={(e) => onChange(e.target.value)}
    className="w-full p-2 border border-gray-300 rounded"
  >
    {options.map((option) => (
      <option key={option.value} value={option.value}>{option.label}</option>
    ))}
  </select>
);

export const SignupForm = () => {
  const [userId, setUserId] = useState("");
  const [password, setPassword] = useState("");
  const [gender, setGender] = useState("male");
  const [birthYear, setBirthYear] = useState<number>();
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const validatePassword = (pwd) => {
    return /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/.test(pwd);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (!validatePassword(password)) {
      setError("비밀번호는 영문+숫자로 이루어진 8글자 이상이어야 합니다.");
      return;
    }

    setLoading(true);

    try {
      // 아이디 중복 검사
      const checkResponse = await DuplicateCheck(userId);

      if (checkResponse.data.exists) {
        setError("이미 사용 중인 유저 아이디입니다.");
        setLoading(false);
        return;
      }

      // 중복되지 않으면 회원가입 데이터 서버에 저장
      const saveResponse = await SaveUserdata(userId, password, birthYear as number, gender);

      if (saveResponse.status === 200) {
        alert("회원가입이 완료되었습니다.");
        setUserId("");
        setPassword("");
        setGender("male");
        setBirthYear(0);
      } else {
        setError("회원가입에 실패했습니다. 다시 시도해주세요.");
      }
    } catch (err) {
      setError("서버와의 통신 중 오류가 발생했습니다.");
    }

    setLoading(false);
  };

  return (
    <div className="bg-gray-500 flex items-center justify-center min-h-screen w-full">
      <div className="bg-white w-[393px] p-6 shadow-lg rounded-lg">
        <p className="text-[40px] text-center text-green-500 font-SBAggroB">
        Hi Book
        </p>
        <p className="text-[60px] text-center text-black font-SBAggroB mb-5">
        GLOVA
        </p>
        <h2 className="text-xl font-bold text-center mb-4">회원가입</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <Label>유저 아이디</Label>
            <Input type="text" value={userId} onChange={(e) => setUserId(e.target.value)} required />
          </div>
          <div>
            <Label>비밀번호</Label>
            <Input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
          </div>
          <div>
            <Label>성별</Label>
            <Select
              value={gender}
              onChange={setGender}
              options={[{ value: "male", label: "남성" }, { value: "female", label: "여성" }]}
            />
          </div>
          <div>
            <Label>출생년도 (YYYY)</Label>
            <Input type="number" value={birthYear} onChange={(e) => setBirthYear(e.target.value)} required />
          </div>
          {error && <p className="text-red-500 text-sm">{error}</p>}
          <button
            type="submit"
            className="w-full p-2 bg-green-600 text-white rounded disabled:bg-gray-400"
            disabled={loading}
          >
            {loading ? "처리 중..." : "회원가입"}
          </button>
        </form>
      </div>
    </div>
  );
}
