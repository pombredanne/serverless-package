import os
from fnmatch import fnmatch

#
# this is the result of calling os.walk on
#
#    moo.txt
#    something.png
#    something.jpg
#    foo/bar.txt
#    foo/baz.txt
#    bar/hello
#    bar/hello.txt
#    bar/nothello
#    a/moo.txt
#    a/goo.txt
#
# given a .gitignore of
#
#    *.jpg
#    foo/
#    bar/hello*
#    moo.txt
#
# the filtered result should be

#   a/goo.txt
#   bar/nothello
#   something.png

walk = [
  [
    ".",
    [
      "foo",
      "bar",
      "a",
    ],
    [
      "moo.txt",        # should be filtered
      "something.png",  # should pass
      "something.jpg",  # should be filtered
    ]
  ],
  [
    "./foo",
    [
    ],
    [
      "bar.txt",    # should be filtered because "foo" is filtered
      "baz.txt",    # should be filtered because "foo" is filtered"
    ],
  ],
  [
    "./bar",
    [
    ],
    [
      "hello",      # should be filtered
      "hello.txt",  # should be filtered
      "nothello",   # should pass
    ],
  ],
  [
    "./a",
    [
    ],
    [
      "moo.txt",      # should be filtered
      "goo.txt",      # should pass
    ],
  ],
]

ignore_files = ['*.jpg', 'foo/', 'bar/hello*', 'moo.txt']
matches = []
for root, dirnames, filenames in walk:
  filenames = [os.path.join(root, filename) for filename in filenames]
  for ignore in ignore_files:
      filenames = [n for n in filenames if not fnmatch(n, ignore)]
  matches.extend(filenames)

print ("\n".join(matches) + "\n")


