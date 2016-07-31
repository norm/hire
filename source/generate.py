from flourish.generators import (
    IndexGenerator,
    PageGenerator,
)


class JobsMixin(object):
    def get_jobs_context_data(self):
        _sources = self.source_objects
        _jobs = _sources.filter(type='employment').order_by('-start')
        return {
            'current_employment': _jobs.filter(end__unset=''),
            'previous_employment': _jobs.filter(end__set=''),
        }


class SkillsMixin(object):
    def get_skills_context_data(self):
        _sources = self.source_objects

        _skills = {}
        for _skill in _sources.filter(type='skill').order_by('position'):
            _class = _skill['class']
            if _class not in _skills:
                _skills[_class] = []
            _skills[_class].append(_skill)

        return _skills


class Summary(SkillsMixin, IndexGenerator):
    template_name = 'summary.html'

    def get_context_data(self):
        _sources = self.source_objects

        _context = super(Summary, self).get_context_data()
        _context.update({
            'introduction': _sources.get('introduction'),
            'skills': self.get_skills_context_data(),
            'values': _sources.get('values'),
        })
        return _context


class JobsIndexPage(JobsMixin, IndexGenerator):
    template_name = 'employment_index.html'

    def get_context_data(self):
        _context = super(JobsIndexPage, self).get_context_data()
        _context.update(self.get_jobs_context_data())
        return _context


class RecommendationsIndexPage(IndexGenerator):
    sources_filter = {'type': 'recommendation'}
    order_by = '-date'
    template_name = 'recommendation_index.html'


class SkillsIndex(SkillsMixin, IndexGenerator):
    sources_filter = {'type': 'skill'}
    order_by = '-date'
    template_name = 'skills_index.html'

    def get_context_data(self):
        _context = super(SkillsIndex, self).get_context_data()
        _context.update({
            'skills': self.get_skills_context_data(),
        })
        return _context


class PrintableSummaryPage(JobsMixin, IndexGenerator):
    template_name = 'printable.html'

    def get_context_data(self):
        _sources = self.source_objects

        _skills = {}
        for _skill in _sources.filter(type='skill').order_by('position'):
            _class = _skill['class']
            if _class not in _skills:
                _skills[_class] = []
            _skills[_class].append(_skill)

        _context = super(PrintableSummaryPage, self).get_context_data()
        _context.update(self.get_jobs_context_data())
        _context.update({
            'skills': _skills,
        })
        return _context


class Page(PageGenerator):
    sources_exclude = {'generate': 'false'}


SOURCE_URL = (
    '/#slug',
    Page.as_generator(),
)

URLS = (
    (
        '/',
        'summary',
        Summary.as_generator(),
    ),
    (
        '/employment/',
        'employment-index',
        JobsIndexPage.as_generator(),
    ),
    (
        '/recommendations/',
        'recommendations-index',
        RecommendationsIndexPage.as_generator(),
    ),
    (
        '/printable',
        'printable',
        PrintableSummaryPage.as_generator(),
    ),
    (
        '/skills/',
        'skills-index',
        SkillsIndex.as_generator(),
    ),
)
