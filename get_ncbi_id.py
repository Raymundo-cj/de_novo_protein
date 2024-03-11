import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.options import Options
import time
import argparse
# this function is to get ncbi web messigion
def fetch_ncbi_protein_info(protein_id):
    ncbi_url = f'https://www.ncbi.nlm.nih.gov/protein/{protein_id}'
    chrom_options = Options()
    chrom_options.add_argument('--headless')
    driver =webdriver.Edge(options=chrom_options)

    try:
        driver.get(ncbi_url)
        time.sleep(10)
        page_source =driver.page_source
 
        soup = BeautifulSoup(page_source, 'html.parser')
        value= str(soup)
        if '/coded_by=' not in value:
            return None
        
        result = value.split('/coded_by="')[1].split('"')[0].strip()
        return result

    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        driver.quit()

def main():
    parser = argparse.ArgumentParser(description="处理蛋白ID信息")
    parser.add_argument("--input","-i",required=True,help="源文件路径")
    parser.add_argument("--output","-o",required=True,help="目标文件路径")

    args = parser.parse_args()
    with open(args.input, 'r') as file:
        protein_ids = [line.strip() for line in file]
    with open(args.output, 'w', encoding='utf-8') as output_file:
        for protein_id in protein_ids:
            protein_info = fetch_ncbi_protein_info(protein_id)
            if protein_info:
                output_file.write(f'{protein_id}\t{protein_info}\n')
                print(f"成功爬取蛋白信息，保存为 {protein_id}文件")
            else:
                print(f"爬取蛋白信息失败 for {protein_id}")
    print(f"结果全部保存")

if __name__ == "__main__":
    main()
