# -*- coding: utf-8 -*-
#
# Copyright © 2012 - 2013 Michal Čihař <michal@cihar.com>
#
# This file is part of Weblate <http://weblate.org/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from django.core.cache import cache


class MachineTranslation(object):
    '''
    Generic object for machine translation services.
    '''
    name = None
    verbose = None

    def __init__(self):
        '''
        Creates new machine translation object.
        '''

    def download_languages(self):
        '''
        Downloads list of supported languages from a service.
        '''
        raise NotImplementedError()

    def download_translations(self, language, text):
        '''
        Downloads list of possible translations from a service.
        '''
        raise NotImplementedError()

    @property
    def supported_languages(self):
        '''
        Returns list of supported languages.
        '''
        cache_key = '%s-languages' % self.name

        # Try using list from cache
        languages = cache.get(cache_key)
        if languages is not None:
            return languages

        # Download
        languages = self.download_languages()

        # Update cache
        cache.set(cache_key, languages, 3600 * 48)

        return languages

    def is_supported(self, language):
        '''
        Checks whether given language combination is supported.
        '''
        return language in self.supported_languages

    def translate(self, language, text):
        '''
        Returns list of machine translations.
        '''
        if not self.is_supported(language):
            return []

        return self.download_translations(language, text)