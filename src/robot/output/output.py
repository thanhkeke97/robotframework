#  Copyright 2008-2015 Nokia Networks
#  Copyright 2016-     Robot Framework Foundation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from . import pyloggingconf
from .debugfile import DebugFile
from .listeners import LibraryListeners, Listeners
from .logger import LOGGER
from .loggerapi import LoggerApi
from .loggerhelper import AbstractLogger
from .loglevel import LogLevel
from .outputfile import OutputFile


class Output(AbstractLogger, LoggerApi):

    def __init__(self, settings):
        self.log_level = LogLevel(settings.log_level)
        self.output_file = OutputFile(
            settings.output,
            self.log_level,
            settings.rpa,
            legacy_output=settings.legacy_output,
        )
        self.listeners = Listeners(settings.listeners, self.log_level)
        self.library_listeners = LibraryListeners(self.log_level)
        self._register_loggers(DebugFile(settings.debug_file))
        self._settings = settings

    @property
    def initial_log_level(self):
        return self._settings.log_level

    def _register_loggers(self, debug_file):
        LOGGER.register_output_file(self.output_file)
        LOGGER.register_listeners(self.listeners or None, self.library_listeners)
        if debug_file:
            LOGGER.register_logger(debug_file)

    def register_error_listener(self, listener):
        LOGGER.register_error_listener(listener)

    @property
    def delayed_logging(self):
        return self.output_file.delayed_logging

    @property
    def delayed_logging_paused(self):
        return self.output_file.delayed_logging_paused

    def close(self, result):
        self.output_file.statistics(result.statistics)
        self.output_file.close()
        LOGGER.unregister_output_file()
        LOGGER.output_file(self._settings["Output"])

    def start_suite(self, data, result):
        LOGGER.start_suite(data, result)

    def end_suite(self, data, result):
        LOGGER.end_suite(data, result)

    def start_test(self, data, result):
        LOGGER.start_test(data, result)

    def end_test(self, data, result):
        LOGGER.end_test(data, result)

    def start_keyword(self, data, result):
        LOGGER.start_keyword(data, result)

    def end_keyword(self, data, result):
        LOGGER.end_keyword(data, result)

    def start_user_keyword(self, data, implementation, result):
        LOGGER.start_user_keyword(data, implementation, result)

    def end_user_keyword(self, data, implementation, result):
        LOGGER.end_user_keyword(data, implementation, result)

    def start_library_keyword(self, data, implementation, result):
        LOGGER.start_library_keyword(data, implementation, result)

    def end_library_keyword(self, data, implementation, result):
        LOGGER.end_library_keyword(data, implementation, result)

    def start_invalid_keyword(self, data, implementation, result):
        LOGGER.start_invalid_keyword(data, implementation, result)

    def end_invalid_keyword(self, data, implementation, result):
        LOGGER.end_invalid_keyword(data, implementation, result)

    def start_for(self, data, result):
        LOGGER.start_for(data, result)

    def end_for(self, data, result):
        LOGGER.end_for(data, result)

    def start_for_iteration(self, data, result):
        LOGGER.start_for_iteration(data, result)

    def end_for_iteration(self, data, result):
        LOGGER.end_for_iteration(data, result)

    def start_while(self, data, result):
        LOGGER.start_while(data, result)

    def end_while(self, data, result):
        LOGGER.end_while(data, result)

    def start_while_iteration(self, data, result):
        LOGGER.start_while_iteration(data, result)

    def end_while_iteration(self, data, result):
        LOGGER.end_while_iteration(data, result)

    def start_group(self, data, result):
        LOGGER.start_group(data, result)

    def end_group(self, data, result):
        LOGGER.end_group(data, result)

    def start_if(self, data, result):
        LOGGER.start_if(data, result)

    def end_if(self, data, result):
        LOGGER.end_if(data, result)

    def start_if_branch(self, data, result):
        LOGGER.start_if_branch(data, result)

    def end_if_branch(self, data, result):
        LOGGER.end_if_branch(data, result)

    def start_try(self, data, result):
        LOGGER.start_try(data, result)

    def end_try(self, data, result):
        LOGGER.end_try(data, result)

    def start_try_branch(self, data, result):
        LOGGER.start_try_branch(data, result)

    def end_try_branch(self, data, result):
        LOGGER.end_try_branch(data, result)

    def start_var(self, data, result):
        LOGGER.start_var(data, result)

    def end_var(self, data, result):
        LOGGER.end_var(data, result)

    def start_break(self, data, result):
        LOGGER.start_break(data, result)

    def end_break(self, data, result):
        LOGGER.end_break(data, result)

    def start_continue(self, data, result):
        LOGGER.start_continue(data, result)

    def end_continue(self, data, result):
        LOGGER.end_continue(data, result)

    def start_return(self, data, result):
        LOGGER.start_return(data, result)

    def end_return(self, data, result):
        LOGGER.end_return(data, result)

    def start_error(self, data, result):
        LOGGER.start_error(data, result)

    def end_error(self, data, result):
        LOGGER.end_error(data, result)

    def message(self, msg):
        LOGGER.log_message(msg)

    def trace(self, msg, write_if_flat=True):
        if write_if_flat or not self.output_file.flatten_level:
            self.write(msg, "TRACE")

    def set_log_level(self, level):
        old = self.log_level.set(level)
        pyloggingconf.set_level(level)
        return old
