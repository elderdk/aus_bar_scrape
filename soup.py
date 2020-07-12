from bs4 import BeautifulSoup
import re

class Soup:
    
    def __init__(self, soup):
        self.soup = soup
        self.clerk_block = soup.find('div', class_='view-display-id-user_profile_clerk_block')
        self.practice_block = soup.find('div', class_='view-area-of-practice')
        self.arbitration_block = soup.find('div', class_='view-display-id-user_arbitration_block')
        self.other_arb_block = soup.find('div', class_='view-display-id-user_other_arbi_block')
        self.jurisdiction_block = soup.find('div', class_='view-display-id-user_juris_block')

    def _parse_num(self, num):
        return num.split(':')[-1].strip()
    
    def get_prof_pic(self):
        try:
            src = self.soup.find('img', src=lambda x: x.startswith('https://www.vicbar.com.au/sites/default/files/styles'))['src']
        except:
            src = None
        finally:
            return src

    def get_full_name(self):
        try:
            full_name = self.soup.find('div', class_='field-name-ds-full-name').get_text().strip()
        except:
            full_name = None
        finally:
            return full_name

    def get_tel(self):
        try:
            tel = self.soup.find('div', class_='field-name-field-internal-phone').get_text().strip()
            tel = self._parse_num(tel)
        except:
            tel = None
        finally:
            return tel

    def get_ext_phone(self):
        try:
            tel = self.soup.find('div', class_='field-name-field-external-phone').get_text().strip()
            tel = self._parse_num(tel)
        except:
            tel = None
        finally:
            return tel

    def get_mob(self):
        try:
            mob = self.soup.find('div', class_='field-name-ds-user-phone').get_text().strip()
            mob = self._parse_num(mob)
        except:
            mob = None
        finally:
            return mob

    def get_fax(self):
        try:
            fax = self.soup.find('div', class_='field-name-field-fax').get_text().strip()
            fax = self._parse_num(fax)
        except:
            fax = None
        finally:
            return fax

    def get_email(self):
        try:
            email = self.soup.find('a', href=re.compile('^mailto:')).get_text().strip()
        except:
            email = None
        finally:
            return email

    def get_chamber(self):
        try:
            chamber = self.soup.find('div', class_='field-name-field-barristers-chamber').get_text().strip()
        except:
            chamber = None
        finally:
            return chamber

    def get_date_of_admission(self):
        try:
            doa = self.soup.find('div', class_='field-name-field-date-of-admission').find_all('div')[1].get_text().strip()
        except:
            doa = None
        finally:
            return doa

    def get_first_signed_bar_roll(self):
        try:
            sbr = self.soup.find('div', class_='field-name-field-date-signed-bar-roll').find_all('div')[1].get_text()
        except:
            sbr = None
        finally:
            return sbr

    def get_date_appointed_silk(self):
        try:
            das = self.soup.find('div', class_='field-name-field-date-appointed-silk').find_all('div')[1].get_text()
        except:
            das = None
        finally:
            return das

    def get_division_bar_roll(self):
        try:
            dbr = self.soup.find('div', class_='field-name-ds-division-of-bar-roll').find_all('div')[1].get_text().strip()
        except:
            dbr = None
        finally:
            return dbr

    def get_qualifications(self):
        try:
            q = self.soup.find('div', class_='field-name-field-qualifications').get_text().strip()
            q = q.split(':')[-1]
        except:
            q = None
        finally:
            return q

    def get_previous_occupation(self):
        try:
            o = self.soup.find('div', class_='field-name-field-previous-occupation').get_text().strip()
        except:
            o = None
        finally:
            return o

    def get_profile(self):
        try:
            prof = self.soup.find('div', string=re.compile('^Profile'))
            prof = prof.next_sibling.get_text()
        except:
            prof = None
        finally:
            return prof

    def get_clerk_title(self):
        try:
            title = self.clerk_block.find('div', class_='views-field-title').get_text().strip()
        except:
            title = None
        finally:
            return title

    def get_clerk_href(self):
        try:
            href = self.clerk_block.find('a', href=re.compile('^http'))['href']
        except:
            href = None
        finally:
            return href

    def get_clerk_phone(self):
        try:
            phone = self.clerk_block.find('div', class_='views-field-field-phone-1')
            phone = phone.get_text().strip()
        except:
            phone = None
        finally:
            return phone

    def get_clerk_email(self):
        try:
            email = self.clerk_block.find('a', href=re.compile('^mailto'))
            email = email.get_text().strip()
        except:
            email = None
        finally:
            return email

    def get_area_of_practice(self):
        try:
            l = [
                    x.get_text().strip() 
                    for x in self.practice_block.select('div.view-content > ul > li > div.views-field.views-field-name > span')
            ]

            l = ', '.join(l)
        except:
            l = None
        finally:
            return l

    def get_arbitration_qualifications(self):
        try:
            l = [
                x.get_text().strip()
                for x in self.arbitration_block.select('div.view-content > div.views-row')
            ]

            l = ', '.join(l)
        except:
            l = None
        finally:
            return l

    def get_other_arb_qualifications(self):
        try:
            l = [
                x.get_text().strip()
                for x in self.other_arb_block.select('div.view-content > div.views-row')
            ]

            l = ', '.join(l)
        except:
            l = None
        finally:
            return l

    def get_jurisdictions(self):
        try:
            l = [
                x.get_text().strip()
                for x in self.jurisdiction_block.select('div.view-content > div.views-row')
            ]

            l = ', '.join(l)
        except:
            l = None
        finally:
            return l
