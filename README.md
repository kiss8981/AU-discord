# AU DISCORD BOT

명령어
--
!도움 일반
- 기본적인 명령어들을 보내드려요!

!도움 음악
- 음악 관련 명령어들을 보내드려요!

!도움 학교
- 학교 관련 명령어들을 보내드려요!

!도움 유틸
- 유틸리티 관련 명령어들을 보내드려요!

!도움 경고
- 경고 관련 명령어들을 보내드려요!

!도움 전적
- 전적 관련 명령어들을 보내드려요!

## 사용된 오픈소스
[경고 오픈소스](https://github.com/Team-EG/j-bot-old)<br>
[롤 전적 오픈소스](https://github.com/J-hoplin1/League-Of-Legend-Search-Bot)<br>
[노래봇 오픈소스](https://github.com/NewPremium/Toaru-kagaku-no-music-bot)<br>
[자가진단 오픈소스](https://github.com/331leo/hcskr_python)

## Note

[Lavalink Download](https://github.com/Frederikam/Lavalink/releases)<br>
[Lavalink Download(for arm or 32bit)](https://github.com/Cog-Creators/Lavalink-Jars/releases)

* 이 프로그램은 [GNU GPL v3.0](https://www.gnu.org/licenses/gpl-3.0.html) 을 따릅니다.

### 참고

* [lavalink.py](https://github.com/Devoxin/Lavalink.py)
* [PythonLavalink](https://github.com/fxrcha/PythonLavalink)
* [EZPaginator](https://github.com/khk4912/EZPaginator)

## How to install

### 컴퓨터로 사용하는 방법

1. `musicbot` 폴더 안에 `config.py` 파일을 만든다.
2. `config.py` 파일을 아래와 같이 작성한다.
```python
from musicbot.sample_config import Config

class Development(Config):
    TOKEN = '토큰'
    OWNERS = [관리자 디스코드 아이디]
    commandInt = "명령인자"
    BOT_NAME = "봇 이름"
    BOT_TAG = "#봇태그"
    BOT_VER = "버전"
    BOT_ID = 봇아이디
    AboutBot = f"""봇 정보(about 명령어)에 넣을 말"""

    # Music
    psw = "컴퓨터 비밀번호"
```
`sample_config.py`를 **참고** 하여 만드시면 됩니다.<br>
3. `python -m musicbot` 명령어를 실행한다.
