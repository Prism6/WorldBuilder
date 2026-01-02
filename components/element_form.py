"""
12요소 편집 폼 컴포넌트.
"""

import streamlit as st
from models.project import Project
from typing import Callable
from utils.logger import get_logger
from constants import ALL_ELEMENT_NAMES

logger = get_logger(__name__)


def render_element_editor(
    element_name: str,
    element_label: str,
    current_description: str,
    on_save: Callable[[str, str], None]
) -> None:
    """
    개별 요소 편집기를 렌더링합니다.

    Args:
        element_name: 요소 이름 (예: 'space', 'time')
        element_label: 표시할 라벨 (예: '🌌 공간')
        current_description: 현재 저장된 설명
        on_save: 저장 콜백 함수
    """
    st.subheader(element_label)

    # 설명 텍스트 영역
    description = st.text_area(
        "설명",
        value=current_description,
        height=300,
        key=f"desc_{element_name}",
        help=f"{element_label} 요소에 대한 상세한 설명을 작성하세요.",
        label_visibility="collapsed"
    )

    # 하단 정보 및 버튼
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        char_count = len(description)
        if char_count > 0:
            st.caption(f"✍️ {char_count}자 작성됨")
        else:
            st.caption("💡 이 요소에 대한 설명을 작성해주세요.")

    with col2:
        if description != current_description:
            st.caption("⚠️ 저장 필요")

    with col3:
        if st.button("💾 저장", key=f"save_{element_name}", use_container_width=True):
            on_save(element_name, description)
            st.success(f"{element_label} 저장 완료!")
            st.rerun()


def render_rules_editor(
    current_natural: list[str],
    current_social: list[str],
    current_religious: list[str],
    on_save: Callable[[list[str], list[str], list[str]], None]
) -> None:
    """
    규칙 요소 편집기를 렌더링합니다 (3개 카테고리).

    Args:
        current_natural: 현재 자연 규칙 목록
        current_social: 현재 사회 규칙 목록
        current_religious: 현재 종교 규칙 목록
        on_save: 저장 콜백 함수
    """
    st.subheader("⚖️ 규칙")
    st.caption("세계의 규칙을 자연법칙, 사회규범, 종교법으로 나누어 작성하세요.")

    # 3개 카테고리를 탭으로 구분
    tab1, tab2, tab3 = st.tabs(["🌿 자연법칙", "👥 사회규범", "⛪ 종교법"])

    with tab1:
        st.markdown("**자연법칙**: 물리적, 생물학적 규칙 (예: 중력, 마법 법칙 등)")
        natural_text = st.text_area(
            "자연법칙 (한 줄에 하나씩 입력)",
            value="\n".join(current_natural),
            height=200,
            key="rules_natural",
            help="각 규칙을 한 줄씩 작성하세요."
        )
        natural_list = [line.strip() for line in natural_text.split("\n") if line.strip()]
        if natural_list:
            st.caption(f"✅ {len(natural_list)}개 규칙 작성됨")

    with tab2:
        st.markdown("**사회규범**: 법률, 관습, 에티켓 등")
        social_text = st.text_area(
            "사회규범 (한 줄에 하나씩 입력)",
            value="\n".join(current_social),
            height=200,
            key="rules_social",
            help="각 규칙을 한 줄씩 작성하세요."
        )
        social_list = [line.strip() for line in social_text.split("\n") if line.strip()]
        if social_list:
            st.caption(f"✅ {len(social_list)}개 규칙 작성됨")

    with tab3:
        st.markdown("**종교법**: 종교적 계율, 금기사항 등")
        religious_text = st.text_area(
            "종교법 (한 줄에 하나씩 입력)",
            value="\n".join(current_religious),
            height=200,
            key="rules_religious",
            help="각 규칙을 한 줄씩 작성하세요."
        )
        religious_list = [line.strip() for line in religious_text.split("\n") if line.strip()]
        if religious_list:
            st.caption(f"✅ {len(religious_list)}개 규칙 작성됨")

    # 저장 버튼
    st.markdown("---")
    col1, col2 = st.columns([3, 1])

    with col1:
        total_rules = len(natural_list) + len(social_list) + len(religious_list)
        if total_rules > 0:
            st.caption(f"📊 총 {total_rules}개의 규칙이 작성되었습니다.")
        else:
            st.caption("💡 최소 하나 이상의 규칙을 작성해주세요.")

    with col2:
        # Check if there are changes
        has_changes = (
            natural_list != current_natural or
            social_list != current_social or
            religious_list != current_religious
        )

        if st.button(
            "💾 저장",
            key="save_rules",
            use_container_width=True,
            type="primary" if has_changes else "secondary"
        ):
            on_save(natural_list, social_list, religious_list)
            st.success("⚖️ 규칙 저장 완료!")
            st.rerun()


def render_element_form(
    project: Project,
    on_update_element: Callable[[str, str], None],
    on_update_rules: Callable[[list[str], list[str], list[str]], None]
) -> None:
    """
    12요소 편집 폼 전체를 렌더링합니다.

    Args:
        project: 현재 프로젝트
        on_update_element: 일반 요소 업데이트 콜백
        on_update_rules: 규칙 요소 업데이트 콜백
    """
    logger.debug(f"Rendering element form for project: {project.project_id}")

    st.title("🌍 12요소 편집")
    st.markdown("세계관을 구성하는 12가지 핵심 요소를 작성하세요.")

    # 진행도 표시
    filled_count = project._count_filled_elements()
    progress = filled_count / 12
    st.progress(progress, text=f"진행도: {filled_count}/12 요소 완료 ({progress*100:.0f}%)")

    st.markdown("---")

    # 요소 라벨 매핑 (dashboard.py와 동일)
    element_labels = {
        'space': '🌌 공간',
        'time': '⏰ 시간',
        'creatures': '👥 생물',
        'nature': '🌿 자연',
        'culture': '🎭 문화',
        'language': '🗣️ 언어',
        'mythology': '⚡ 신화',
        'philosophy': '💭 철학',
        'rules': '⚖️ 규칙',
        'economy': '💰 경제',
        'politics': '🏛️ 정치',
        'energy': '✨ 에너지'
    }

    # 12개 요소를 탭으로 표시
    tab_labels = [element_labels[name] for name in ALL_ELEMENT_NAMES]
    tabs = st.tabs(tab_labels)

    # 각 탭에 해당하는 요소 편집기 렌더링
    for idx, element_name in enumerate(ALL_ELEMENT_NAMES):
        with tabs[idx]:
            if element_name == 'rules':
                # 규칙은 특수 처리
                render_rules_editor(
                    current_natural=project.elements.rules.natural,
                    current_social=project.elements.rules.social,
                    current_religious=project.elements.rules.religious,
                    on_save=on_update_rules
                )
            else:
                # 일반 요소
                element = getattr(project.elements, element_name)
                render_element_editor(
                    element_name=element_name,
                    element_label=element_labels[element_name],
                    current_description=element.description,
                    on_save=on_update_element
                )

    # 하단 도움말
    st.markdown("---")
    with st.expander("💡 작성 팁"):
        st.markdown("""
        **효과적인 세계관 구축을 위한 팁**:

        1. **일관성 유지**: 각 요소들이 서로 모순되지 않도록 주의하세요.
        2. **구체적으로 작성**: 추상적인 설명보다는 구체적인 예시를 포함하세요.
        3. **독창성**: 기존 세계관과 차별화되는 독특한 요소를 추가하세요.
        4. **필요한 만큼만**: 모든 요소를 과도하게 상세히 작성할 필요는 없습니다.
        5. **반복 수정**: 작성 후 다시 읽고 수정하면서 완성도를 높이세요.

        **12요소 간 연결 관계**:
        - 공간 ↔ 시간: 역사적 사건이 지리에 영향
        - 생물 ↔ 자연: 환경이 생물의 진화에 영향
        - 문화 ↔ 언어: 언어가 문화를 반영
        - 신화 ↔ 철학: 신화가 가치관 형성에 영향
        - 규칙 ↔ 정치: 법률과 통치 시스템 연계
        - 경제 ↔ 에너지: 자원이 경제 구조 결정
        """)
