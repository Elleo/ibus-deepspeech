# vim:set noet ts=4:
#
# ibus-deepspeech - Speech recognition engine for IBus
#
# Copyright (c) 2017 Mike Sheldon <elleo@gnu.org>
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

engine_deepspeech_PYTHON = \
	engine.py \
	main.py \
	$(NULL)
engine_deepspeechdir = $(datadir)/ibus-deepspeech

libexec_SCRIPTS = ibus-engine-deepspeech

component_DATA = deepspeech.xml
componentdir = $(datadir)/ibus/component

CLEANFILES = \
	*.pyc \
	$(NULL)

EXTRA_DIST = \
	ibus-engine-deepspeech.in \
	deepspeech.xml.in.in \
	$(NULL)

deepspeech.xml: deepspeech.xml.in
	$(AM_V_GEN) \
	( \
		libexecdir=${libexecdir}; \
		pkgdatadir=${pkgdatadir}; \
		s=`cat $<`; \
		eval "echo \"$${s}\""; \
	) > $@

test:
	$(ENV) \
		LANG=en_US \
		PYTHONPATH=$(top_srcdir) \
		$(PYTHON) $(srcdir)/main.py

