"""Tests for the converter module."""

from nic2markdown.converter import convert


class TestHeadings:
    def test_h1(self):
        md = convert("<h1>Hello</h1>")
        assert md.strip() == "# Hello"

    def test_h2(self):
        md = convert("<h2>Section</h2>")
        assert md.strip() == "## Section"

    def test_heading_with_strong_unwrapped(self):
        md = convert("<h1><strong>Bold Title</strong></h1>")
        assert md.strip() == "# Bold Title"


class TestParagraphsAndInline:
    def test_paragraph(self):
        md = convert("<p>Hello world</p>")
        assert md.strip() == "Hello world"

    def test_bold(self):
        md = convert("<p><strong>bold</strong> text</p>")
        assert md.strip() == "**bold** text"

    def test_italic(self):
        md = convert("<p><em>italic</em> text</p>")
        assert md.strip() == "*italic* text"

    def test_inline_code(self):
        md = convert("<p>Use <code>cmd</code> now</p>")
        assert "`cmd`" in md

    def test_link(self):
        md = convert('<p><a href="https://example.com">click</a></p>')
        assert "[click](https://example.com)" in md


class TestCodeBlocks:
    def test_fenced_code_block(self):
        html = '<div class="highlight"><pre><span></span><code>print("hello")\n</code></pre></div>'
        md = convert(html)
        assert "```" in md
        assert 'print("hello")' in md


class TestAdmonitions:
    def test_note(self):
        html = (
            '<div class="admonition note">'
            '<p class="admonition-title">Note Title</p>'
            '<p>Some content.</p>'
            '</div>'
        )
        md = convert(html)
        assert "> [!NOTE]" in md
        assert "**Note Title**" in md
        assert "Some content." in md

    def test_warning(self):
        html = (
            '<div class="admonition warning">'
            '<p class="admonition-title">Careful</p>'
            '<p>Watch out.</p>'
            '</div>'
        )
        md = convert(html)
        assert "> [!WARNING]" in md
        assert "**Careful**" in md

    def test_danger(self):
        html = (
            '<div class="admonition danger">'
            '<p class="admonition-title">Danger</p>'
            '<p>Do not proceed.</p>'
            '</div>'
        )
        md = convert(html)
        assert "> [!CAUTION]" in md

    def test_tip(self):
        html = (
            '<div class="admonition tip">'
            '<p class="admonition-title">Pro Tip</p>'
            '<p>Use this trick.</p>'
            '</div>'
        )
        md = convert(html)
        assert "> [!TIP]" in md

    def test_success(self):
        html = (
            '<div class="admonition success">'
            '<p class="admonition-title">Done</p>'
            '<p>It worked.</p>'
            '</div>'
        )
        md = convert(html)
        assert "> [!TIP]" in md

    def test_info_as_note(self):
        html = (
            '<div class="admonition info">'
            '<p class="admonition-title">FYI</p>'
            '<p>Just so you know.</p>'
            '</div>'
        )
        md = convert(html)
        assert "> [!NOTE]" in md

    def test_question_as_important(self):
        html = (
            '<div class="admonition question">'
            '<p class="admonition-title">Q</p>'
            '<p>Why?</p>'
            '</div>'
        )
        md = convert(html)
        assert "> [!IMPORTANT]" in md


class TestTaskLists:
    def test_unchecked(self):
        html = (
            '<ul class="task-list">'
            '<li class="task-list-item">'
            '<label class="task-list-control">'
            '<input type="checkbox" disabled/>'
            '<span class="task-list-indicator"></span>'
            '</label>'
            'Do something'
            '</li>'
            '</ul>'
        )
        md = convert(html)
        assert "[ ]" in md
        assert "Do something" in md

    def test_checked(self):
        html = (
            '<ul class="task-list">'
            '<li class="task-list-item">'
            '<label class="task-list-control">'
            '<input type="checkbox" disabled checked/>'
            '<span class="task-list-indicator"></span>'
            '</label>'
            'Done'
            '</li>'
            '</ul>'
        )
        md = convert(html)
        assert "[x]" in md
        assert "Done" in md


class TestHeaderlinkRemoval:
    def test_headerlink_removed(self):
        html = '<h1 id="test">Title<a class="headerlink" href="#test">&para;</a></h1>'
        md = convert(html)
        assert "headerlink" not in md
        assert "&para;" not in md
        assert "# Title" in md


class TestTables:
    def test_simple_table(self):
        html = (
            '<table>'
            '<thead><tr><th>A</th><th>B</th></tr></thead>'
            '<tbody><tr><td>1</td><td>2</td></tr></tbody>'
            '</table>'
        )
        md = convert(html)
        assert "| A | B |" in md
        assert "| 1 | 2 |" in md


class TestRelativeLinkFixing:
    def test_absolute_url_unchanged(self):
        md = convert(
            '<p><a href="https://other.com/page">link</a></p>',
            base_url="https://example.com/docs/"
        )
        assert "[link](https://other.com/page)" in md

    def test_relative_url_fixed(self):
        md = convert(
            '<p><a href="next.html">next</a></p>',
            base_url="https://example.com/docs/page/"
        )
        assert "[next](https://example.com/docs/page/next.html)" in md
