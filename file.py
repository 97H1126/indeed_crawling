def save_to_file(file_name, jobs):
    with open(f"{file_name}.csv", "w",encoding="utf-8") as file: # with를 사용햐여 파일의 열고 닫음을 자동으로 처리하고 코드를 간결하게
        file.write("직무,회사,지역,회사공고url\n")  # 열 제목(헤더) 추가

        for job in jobs:
            row = f"{job['직무']},{job['회사']},{job['위치']},{job['회사공고url']}\n"
            file.write(row)
