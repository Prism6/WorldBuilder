# components/connections.py
"""
Connection management component for visualizing and editing relationships
between world elements.
"""

import streamlit as st
import plotly.graph_objects as go
import math
from typing import Callable, Dict, Any, List
from models.project import Project


# 12요소 이름과 라벨 매핑
ELEMENT_LABELS = {
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

# 연결 관계 타입
CONNECTION_TYPES = {
    'influences': '→ 영향을 준다',
    'depends_on': '⇆ 의존한다',
    'conflicts': '⚔️ 충돌한다',
    'harmonizes': '🤝 조화를 이룬다',
    'causes': '⚡ 원인이 된다',
    'enables': '🔓 가능하게 한다'
}

# 연결 타입별 색상
CONNECTION_COLORS = {
    'influences': '#3B82F6',      # Blue
    'depends_on': '#8B5CF6',      # Purple
    'conflicts': '#EF4444',       # Red
    'harmonizes': '#10B981',      # Green
    'causes': '#F59E0B',          # Amber
    'enables': '#EC4899'          # Pink
}


def create_network_graph(connections: List[Dict[str, Any]]) -> go.Figure:
    """
    Create an interactive network graph visualization of connections.

    Args:
        connections: List of connection dictionaries

    Returns:
        Plotly figure object
    """
    # Get list of elements
    elements = list(ELEMENT_LABELS.keys())
    n_elements = len(elements)

    # Calculate circular positions for nodes
    node_x = []
    node_y = []
    node_text = []

    radius = 1.0
    for i, element in enumerate(elements):
        angle = 2 * math.pi * i / n_elements - math.pi / 2  # Start at top
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        node_x.append(x)
        node_y.append(y)
        node_text.append(ELEMENT_LABELS[element])

    # Create node positions dict for easy lookup
    node_pos = {element: (node_x[i], node_y[i]) for i, element in enumerate(elements)}

    # Create edge traces (one trace per connection type for coloring)
    edge_traces = []

    for conn_type, color in CONNECTION_COLORS.items():
        # Filter connections of this type
        type_connections = [c for c in connections if c.get('connection_type') == conn_type]

        if not type_connections:
            continue

        edge_x = []
        edge_y = []
        edge_text = []

        for conn in type_connections:
            from_elem = conn.get('from_element', '')
            to_elem = conn.get('to_element', '')

            if from_elem not in node_pos or to_elem not in node_pos:
                continue

            x0, y0 = node_pos[from_elem]
            x1, y1 = node_pos[to_elem]

            # Add edge line
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

            # Prepare hover text
            desc = conn.get('description', '설명 없음')
            hover = f"{ELEMENT_LABELS[from_elem]} → {ELEMENT_LABELS[to_elem]}<br>{desc}"
            edge_text.append(hover)

        # Create edge trace
        edge_trace = go.Scatter(
            x=edge_x,
            y=edge_y,
            mode='lines',
            line=dict(width=2, color=color),
            hoverinfo='text',
            text=edge_text,
            name=CONNECTION_TYPES[conn_type],
            showlegend=True
        )
        edge_traces.append(edge_trace)

    # Create node trace
    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers+text',
        hoverinfo='text',
        text=node_text,
        textposition="middle center",
        textfont=dict(size=10, color='white'),
        marker=dict(
            size=50,
            color='#1E293B',
            line=dict(width=2, color='#475569')
        ),
        showlegend=False,
        hovertext=node_text
    )

    # Create figure
    fig = go.Figure(data=edge_traces + [node_trace])

    # Update layout
    fig.update_layout(
        title="연결 관계 네트워크",
        showlegend=True,
        hovermode='closest',
        margin=dict(b=20, l=5, r=5, t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=600,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        )
    )

    return fig


def render_network_graph(connections: List[Dict[str, Any]]) -> None:
    """
    Render the network graph visualization.

    Args:
        connections: List of connections to visualize
    """
    if not connections:
        st.info("💡 연결 관계를 추가하면 네트워크 그래프가 표시됩니다.")
        return

    st.subheader("🕸️ 연결 관계 네트워크")
    st.caption(f"{len(connections)}개의 연결 관계를 시각화하고 있습니다.")

    # Create and display graph
    fig = create_network_graph(connections)
    st.plotly_chart(fig, use_container_width=True)

    # Graph legend explanation
    with st.expander("ℹ️ 그래프 설명"):
        st.markdown("""
        **네트워크 그래프 읽는 법**:

        - **노드 (원)**: 12가지 세계관 요소
        - **엣지 (선)**: 요소 간 연결 관계
        - **색상**: 연결 관계의 타입

        **상호작용**:
        - 선 위에 마우스를 올리면 연결 상세 정보를 볼 수 있습니다
        - 범례를 클릭하여 특정 관계 타입을 표시/숨김할 수 있습니다
        - 확대/축소 및 드래그가 가능합니다

        **팁**:
        - 중심에 가까운 요소일수록 많은 연결을 가집니다
        - 같은 색상의 선이 많으면 해당 관계 타입이 지배적입니다
        """)


def render_connection_card(
    connection: Dict[str, Any],
    index: int,
    on_delete: Callable[[int], None]
) -> None:
    """
    Render a single connection as a card.

    Args:
        connection: Connection dictionary
        index: Index of the connection in the list
        on_delete: Callback to delete the connection
    """
    from_label = ELEMENT_LABELS.get(connection.get('from_element', ''), '???')
    to_label = ELEMENT_LABELS.get(connection.get('to_element', ''), '???')
    conn_type = connection.get('connection_type', 'influences')
    type_label = CONNECTION_TYPES.get(conn_type, '→')
    description = connection.get('description', '')

    # Card container
    with st.container():
        col1, col2 = st.columns([5, 1])

        with col1:
            # Connection summary
            st.markdown(f"**{from_label}** {type_label} **{to_label}**")
            if description:
                st.caption(description)

        with col2:
            # Delete button
            if st.button("🗑️", key=f"del_conn_{index}", help="연결 삭제"):
                on_delete(index)
                st.rerun()

        st.divider()


def render_connection_form(
    on_add: Callable[[Dict[str, Any]], None]
) -> None:
    """
    Render form to add a new connection.

    Args:
        on_add: Callback to add a new connection
    """
    st.subheader("➕ 새 연결 관계 추가")

    with st.form("add_connection_form"):
        col1, col2 = st.columns(2)

        with col1:
            from_element = st.selectbox(
                "시작 요소",
                options=list(ELEMENT_LABELS.keys()),
                format_func=lambda x: ELEMENT_LABELS[x],
                key="from_element"
            )

        with col2:
            to_element = st.selectbox(
                "대상 요소",
                options=list(ELEMENT_LABELS.keys()),
                format_func=lambda x: ELEMENT_LABELS[x],
                key="to_element"
            )

        connection_type = st.selectbox(
            "관계 유형",
            options=list(CONNECTION_TYPES.keys()),
            format_func=lambda x: CONNECTION_TYPES[x],
            key="connection_type"
        )

        description = st.text_area(
            "관계 설명 (선택)",
            placeholder="이 두 요소가 어떻게 연결되어 있는지 설명해주세요...",
            height=100,
            max_chars=500,
            key="connection_description"
        )

        submitted = st.form_submit_button("✅ 연결 추가", type="primary")

        if submitted:
            # Validation
            if from_element == to_element:
                st.error("❌ 같은 요소끼리는 연결할 수 없습니다.")
            else:
                # Create connection
                new_connection = {
                    'from_element': from_element,
                    'to_element': to_element,
                    'connection_type': connection_type,
                    'description': description.strip()
                }
                on_add(new_connection)
                st.success(f"✅ 연결이 추가되었습니다: {ELEMENT_LABELS[from_element]} {CONNECTION_TYPES[connection_type]} {ELEMENT_LABELS[to_element]}")
                st.rerun()


def render_connection_stats(connections: List[Dict[str, Any]]) -> None:
    """
    Render statistics about connections.

    Args:
        connections: List of all connections
    """
    total = len(connections)

    if total == 0:
        st.info("💡 아직 연결 관계가 없습니다. 12요소 간의 관계를 추가해보세요!")
        return

    # Count by type
    type_counts: Dict[str, int] = {}
    for conn in connections:
        conn_type = conn.get('connection_type', 'influences')
        type_counts[conn_type] = type_counts.get(conn_type, 0) + 1

    # Display stats
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("총 연결 수", total)

    with col2:
        most_common = max(type_counts.items(), key=lambda x: x[1]) if type_counts else ('influences', 0)
        st.metric("가장 많은 관계", CONNECTION_TYPES.get(most_common[0], '→'))

    with col3:
        # Count elements involved
        elements_involved = set()
        for conn in connections:
            elements_involved.add(conn.get('from_element', ''))
            elements_involved.add(conn.get('to_element', ''))
        st.metric("연결된 요소", f"{len(elements_involved)}/12")


def render_connection_list(
    connections: List[Dict[str, Any]],
    on_delete: Callable[[int], None]
) -> None:
    """
    Render list of all connections.

    Args:
        connections: List of connections
        on_delete: Callback to delete a connection
    """
    if not connections:
        st.info("💡 연결 관계를 추가하면 여기에 표시됩니다.")
        return

    st.subheader(f"🔗 연결 관계 목록 ({len(connections)}개)")

    # Filter by connection type
    filter_type = st.selectbox(
        "관계 유형으로 필터링",
        options=['all'] + list(CONNECTION_TYPES.keys()),
        format_func=lambda x: "전체 보기" if x == 'all' else CONNECTION_TYPES[x],
        key="filter_type"
    )

    # Filter connections
    filtered = connections if filter_type == 'all' else [
        c for c in connections if c.get('connection_type') == filter_type
    ]

    if not filtered:
        st.info(f"선택한 유형의 연결이 없습니다.")
        return

    st.caption(f"{len(filtered)}개의 연결이 표시되고 있습니다.")

    # Render each connection
    for i, conn in enumerate(filtered):
        # Find original index for deletion
        original_idx = connections.index(conn)
        render_connection_card(conn, original_idx, on_delete)


def render_connection_tips() -> None:
    """Render helpful tips for creating connections."""
    with st.expander("💡 연결 관계 작성 팁"):
        st.markdown("""
        **효과적인 연결 관계 구축 방법**:

        1. **인과관계 파악하기**
           - 어떤 요소가 다른 요소에 영향을 주나요?
           - 예: 공간(지형) → 문화(생활 방식)

        2. **의존성 찾기**
           - 어떤 요소가 다른 요소에 의존하나요?
           - 예: 경제 ⇆ 정치 (상호 의존)

        3. **충돌과 조화**
           - 서로 갈등하는 요소가 있나요?
           - 예: 신화 ⚔️ 철학 (신앙 vs 이성)
           - 서로 보완하는 요소가 있나요?
           - 예: 자연 🤝 에너지 (자연 에너지 활용)

        4. **연결이 많을수록 풍부한 세계관**
           - 최소 5-10개의 연결을 만들어보세요
           - 각 요소가 최소 1개 이상의 연결을 가지도록 하세요

        5. **설명 추가하기**
           - 왜 이 두 요소가 연결되어 있는지 간단히 설명하세요
           - 구체적인 예시를 들면 더 좋습니다
        """)


def render_connections_page(
    project: Project,
    on_add_connection: Callable[[Dict[str, Any]], None],
    on_delete_connection: Callable[[int], None]
) -> None:
    """
    Render the complete connections page.

    Args:
        project: Current project
        on_add_connection: Callback to add a connection
        on_delete_connection: Callback to delete a connection
    """
    st.title("🔗 연결 관계")
    st.markdown("12요소 간의 관계를 정의하여 세계관의 깊이를 더하세요.")

    # Statistics
    render_connection_stats(project.connections)

    st.divider()

    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["📋 목록 보기", "🕸️ 그래프 보기", "➕ 연결 추가"])

    with tab1:
        # Connection list
        render_connection_list(project.connections, on_delete_connection)

    with tab2:
        # Network graph visualization
        render_network_graph(project.connections)

    with tab3:
        # Add connection form
        render_connection_form(on_add_connection)

    st.divider()

    # Tips
    render_connection_tips()
