"""
간단한 리팩토링 검증 스크립트
"""

from repositories.json_project_repository import JsonProjectRepository
from services.project_manager import ProjectManager
from exceptions import ProjectValidationError, ProjectNotFoundException
import os
import shutil

# 테스트용 디렉토리 설정
TEST_DIR = "data/test_projects"

def cleanup_test_dir():
    """테스트 디렉토리 정리"""
    if os.path.exists(TEST_DIR):
        shutil.rmtree(TEST_DIR)
    os.makedirs(TEST_DIR, exist_ok=True)

def test_create_and_save_project():
    """프로젝트 생성 및 저장 테스트"""
    print("1. 프로젝트 생성 및 저장 테스트...")

    # Repository와 Service 초기화
    repository = JsonProjectRepository(storage_dir=TEST_DIR)
    manager = ProjectManager(repository=repository)

    # 새 프로젝트 생성
    project = manager.create_new_project(
        project_name="테스트 세계",
        genre="판타지"
    )

    print(f"   [OK] 프로젝트 생성됨: {project.project_name}")
    print(f"   [OK] 프로젝트 ID: {project.project_id}")

    # 프로젝트 저장
    success = manager.save_project(project)
    assert success, "프로젝트 저장 실패"
    print(f"   [OK] 프로젝트 저장 성공")

    return project.project_id

def test_load_project(project_id):
    """프로젝트 로드 테스트"""
    print("\n2. 프로젝트 로드 테스트...")

    repository = JsonProjectRepository(storage_dir=TEST_DIR)
    manager = ProjectManager(repository=repository)

    # 프로젝트 로드
    project = manager.load_project(project_id)
    assert project is not None, "프로젝트 로드 실패"
    assert project.project_name == "테스트 세계", "프로젝트 이름 불일치"

    print(f"   [OK] 프로젝트 로드 성공: {project.project_name}")
    return project

def test_update_metadata(project):
    """메타데이터 업데이트 테스트"""
    print("\n3. 메타데이터 업데이트 테스트...")

    repository = JsonProjectRepository(storage_dir=TEST_DIR)
    manager = ProjectManager(repository=repository)

    # 메타데이터 업데이트
    manager.update_project_metadata(
        project,
        project_name="업데이트된 세계",
        genre="SF"
    )

    assert project.project_name == "업데이트된 세계", "프로젝트 이름 업데이트 실패"
    assert project.genre == "SF", "장르 업데이트 실패"

    print(f"   [OK] 프로젝트 이름 업데이트: {project.project_name}")
    print(f"   [OK] 장르 업데이트: {project.genre}")

    # 업데이트된 프로젝트 저장
    manager.save_project(project)
    print(f"   [OK] 업데이트된 프로젝트 저장 성공")

def test_update_element(project):
    """요소 업데이트 테스트"""
    print("\n4. 월드 요소 업데이트 테스트...")

    repository = JsonProjectRepository(storage_dir=TEST_DIR)
    manager = ProjectManager(repository=repository)

    # Space 요소 업데이트
    manager.update_project_element(
        project,
        element_name="space",
        description="광활한 우주 공간에 펼쳐진 세계"
    )

    assert project.elements.space.description == "광활한 우주 공간에 펼쳐진 세계", "Space 요소 업데이트 실패"

    print(f"   [OK] Space 요소 업데이트 성공")

    # Time 요소 업데이트
    manager.update_project_element(
        project,
        element_name="time",
        description="미래 시대, 2500년대"
    )

    print(f"   [OK] Time 요소 업데이트 성공")

    # 완성도 확인
    completion_rate = manager.get_project_completion_rate(project)
    print(f"   [OK] 현재 완성도: {completion_rate * 100:.1f}%")

    # 저장
    manager.save_project(project)
    print(f"   [OK] 업데이트된 프로젝트 저장 성공")

def test_validation():
    """유효성 검증 테스트"""
    print("\n5. 유효성 검증 테스트...")

    repository = JsonProjectRepository(storage_dir=TEST_DIR)
    manager = ProjectManager(repository=repository)

    try:
        # 빈 프로젝트 이름으로 생성 시도
        project = manager.create_new_project(project_name="")
        print("   [FAIL] 유효성 검증 실패 (빈 이름이 허용됨)")
    except ProjectValidationError:
        print("   [OK] 빈 프로젝트 이름 검증 성공")

    # 정상 프로젝트 생성
    project = manager.create_new_project(project_name="검증 테스트")

    try:
        # 빈 이름으로 업데이트 시도
        manager.update_project_metadata(project, project_name="")
        print("   [FAIL] 유효성 검증 실패 (빈 이름으로 업데이트됨)")
    except ProjectValidationError:
        print("   [OK] 빈 이름 업데이트 검증 성공")

def test_list_projects():
    """프로젝트 목록 조회 테스트"""
    print("\n6. 프로젝트 목록 조회 테스트...")

    repository = JsonProjectRepository(storage_dir=TEST_DIR)
    manager = ProjectManager(repository=repository)

    projects = manager.list_all_projects()
    print(f"   [OK] 총 {len(projects)}개의 프로젝트 발견")

    for project_id, project_name in projects.items():
        print(f"     - {project_name} (ID: {project_id[:8]}...)")

def test_not_found():
    """존재하지 않는 프로젝트 테스트"""
    print("\n7. 존재하지 않는 프로젝트 테스트...")

    repository = JsonProjectRepository(storage_dir=TEST_DIR)
    manager = ProjectManager(repository=repository)

    try:
        manager.load_project("non-existent-id")
        print("   [FAIL] 예외 처리 실패")
    except ProjectNotFoundException:
        print("   [OK] ProjectNotFoundException 발생 성공")

def main():
    """메인 테스트 함수"""
    print("=" * 60)
    print("리팩토링 검증 테스트 시작")
    print("=" * 60)

    try:
        # 테스트 디렉토리 초기화
        cleanup_test_dir()

        # 테스트 실행
        project_id = test_create_and_save_project()
        project = test_load_project(project_id)
        test_update_metadata(project)
        test_update_element(project)
        test_validation()
        test_list_projects()
        test_not_found()

        print("\n" + "=" * 60)
        print("모든 테스트 통과!")
        print("=" * 60)

        # 정리
        print("\n테스트 디렉토리 정리 중...")
        cleanup_test_dir()
        print("완료!")

    except Exception as e:
        print(f"\n테스트 실패: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
