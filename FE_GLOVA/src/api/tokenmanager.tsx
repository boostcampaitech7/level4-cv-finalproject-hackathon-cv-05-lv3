import { useEffect } from "react";
import { StartTokenRefresh, StopTokenRefresh } from "./cookies"; // 위에서 만든 함수 가져오기

const TokenManager = () => {
    useEffect(() => {
        StartTokenRefresh(); // 컴포넌트가 마운트되면 자동 실행

        return () => StopTokenRefresh(); // 언마운트 시 자동 정리
    }, []);

    return null; // UI 요소 없음
};

export default TokenManager;
