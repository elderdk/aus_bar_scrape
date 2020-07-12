from constants import *
import requests
from bs4 import BeautifulSoup
import concurrent.futures
import threading
from timeit import timeit
import os
from soup import Soup
import pandas as pd
from collections import OrderedDict


class VicBar:

    def __init__(self):
        self.url_base = VIC_BAR_BASE
        self.first_page = VIC_BAR
        self.headers = {'user-agent': USER_AGENT}
        self.lock = threading.Lock()
        self.df = pd.DataFrame(columns=COLUMNS)
    
    def _get_last_page(self) -> int:
        first_page = self.first_page
        headers = self.headers
        html = requests.get(first_page, headers=headers).text
        soup = BeautifulSoup(html, 'html.parser')
        search_base = soup.find('a', title='Go to last page', href=True)['href']
        last_page = search_base.split('page=')[-1]
        search_href = '&'.join(search_base.split('&')[:-1]) + '&page='     

        return search_href, int(last_page)

    def _get_profile_hrefs(self) -> list:
        search_href, last_page = self._get_last_page()
        base_url = self.url_base
        headers = self.headers

        hrefs_list = [base_url + search_href + str(page + 1) for page in range(last_page)]
        hrefs_list.append(VIC_BAR)

        prof_href_list = []

        def parse_page(href):
            html = requests.get(href, headers=headers).text
            soup = BeautifulSoup(html, 'html.parser')
            profs = soup.find_all('a', class_='pre_render_alter', href=True)
            l = [prof['href'] for prof in profs]

            with self.lock:
                prof_href_list.extend(l)

        start_time = timeit()

        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as e:
            e.map(parse_page, hrefs_list)

        print(f"Total {len(prof_href_list)} profiles gathered in {timeit() - start_time} seconds.")

        return prof_href_list

    def _make_df(self, url) -> pd.DataFrame:
        print(f'getting {url}')
        html = requests.get(url, headers=self.headers).text
        soup = BeautifulSoup(html, 'html.parser')
        s = Soup(soup)

        d = OrderedDict([
            ('prof_url', url),
            ('prof_pic', s.get_prof_pic()),
            ('full_name', s.get_full_name()),
            ('tel', s.get_tel()),
            ('ext_phone', s.get_ext_phone()),
            ('mob', s.get_mob()),
            ('fax', s.get_fax()),
            ('email', s.get_email()),
            ('chamber', s.get_chamber()),
            ('date_of_admission', s.get_date_of_admission()),
            ('first_signed_bar_roll', s.get_first_signed_bar_roll()),
            ('date_appointed_silk', s.get_date_appointed_silk()),
            ('division_of_bar_roll', s.get_division_bar_roll()),
            ('qualifications', s.get_qualifications()),
            ('previous_occupation', s.get_previous_occupation()),
            ('profile', s.get_profile()),
            ('clerk_title', s.get_clerk_title()),
            ('clerk_href', s.get_clerk_href()),
            ('clerk_phone', s.get_clerk_phone()),
            ('clerk_email', s.get_clerk_email()),
            ('area_of_practice', s.get_area_of_practice()),
            ('arbitration_qualifications', s.get_arbitration_qualifications()),
            ('other_arbitration_qualifications', s.get_other_arb_qualifications()),
            ('jurisdictions', s.get_jurisdictions())
        ])

        with self.lock:
            self.df = self.df.append(d, ignore_index=True)

        return self.df

    def _parse_profiles(self):
        profiles = [VIC_BAR_BASE + profile[1:] for profile in self._get_profile_hrefs()]

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as e:
            e.map(self._make_df, profiles[:100])
        
        return self.df

    def save_to_excel(self):
        df = self._parse_profiles()

        dirname = os.path.dirname(os.path.realpath(__file__))
        file_name = 'result.xlsx'
        excel_file = os.path.join(dirname, file_name)
        df.to_excel(excel_file)


v = VicBar()
v.save_to_excel()
