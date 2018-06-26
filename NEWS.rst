0.7.2 (2018-06-24):
  Minor:

  - Fix ``epsilon.benchmark`` compatibility with newer *Twisted* versions.
  - Add explicit dependency on ``zope.interface``.

0.7.1 (2015-10-10):
  Major:

  - *certcreate* should now be installed properly.
  - An ``asRFC1123`` method was added to ``extime.Time``.
  - As *Twisted* is dropping Python 2.6, Epsilon will also not support 2.6 from
    the next release.

  Minor:

  - ``epsilon.benchmark`` now uses ``/proc/self/mounts`` instead of relying on
    ``/etc/mtab`` which is often wrong, or does not even exist.
  - Fixed a test that interacted badly with *Twisted* 15.4.0.
  - Updated the metadata in *setup.py*.

0.7.0 (2014-01-15):
  Major:

  - Only *Python* 2.6 and 2.7 are supported now. 2.4, 2.5 is deprecated.
  - setup.py now uses setuptools, and stores its dependencies. This
    means you no longer need to manually install dependencies.
  - *setup.py* no longer requires *Twisted* for *egg_info*, making it easier
    to install *Epsilon* using *pip*.
  - Significant improvements to *PyPy* support. *PyPy* is now a supported
    platform, with CI support.
  - ``epsilon.release`` is now removed. It relied on a bunch of machinery
    specific to *Divmod* that no longer existed.
  - ``epsilon.sslverify`` is now removed. Use ``twisted.internet.ssl`` instead.
  - ``epsilon.asTwistedVersion`` takes a string version (``"1.2.3"``) and
    turns it into a ``twisted.python.versions.Version``.

  Minor:

  - Several deprecation warnings have been cleaned up.

0.6.0 (2009-11-25):
  - Disable loopback hotfix on *Twisted* 8.2 and newer.
  - Remove the implementation of ``Cooperator`` and use *Twisted*'s
    implementation instead.
  - Use *Twisted*'s ``deferLater`` implementation.
  - Add a service for communicating via *stdio*.
  - Add a ``precision`` argument to ``Time.asHumanly`` to control the precision
    of the returned string.

0.5.12 (2008-12-09):
  - Added support for *AMP* authentication via one-time pads.

0.5.11 (2008-10-02):
  - ``epsilon.amprouter`` added, providing support for multiplexing
    unrelated *AMP* communications over the same connection.

0.5.10 (2008-08-12):
  - Added the ``epsilon.caseless`` module, with case-insensitive string
    wrappers.
  - Better ``repr()`` for ``epsilon.structlike.record`` added.
  - ``epsilon.juice`` now uses ``twisted.internet.ssl`` instead of
    ``epsilon.sslverify``.

0.5.9 (2008-01-18):
  - No noted changes.

0.5.8 (2007-11-27):
  - ``extime.Time.asHumanly`` no longer shows a time of day for all-day
    timestamps.

0.5.7 (2007-04-27):
  - ``view.SlicedView`` added, allowing slicing and indexing of large
    sequences without copying.

0.5.6 (2006-11-20):
  - Added a ``--quiet`` option to *Epsilon's* *certcreate* and use it in a few
    unit tests to avoid spewing garbage during test runs.

0.5.5 (2006-10-21):
  - ``extime.Time`` now accepts RFC2822-like dates with invalid fields: it
    rounds them to the nearest valid value.

0.5.4 (2006-10-17):
  - ``extime.Time`` now accepts RFC2822-like dates with no timezone.

0.5.3 (2006-09-20):
  - ``structlike.Record`` now raises ``TypeError`` on unexpected args.

0.5.2 (2006-09-12):
  - ``extime.Time`` now avoids ``time_t`` overflow bugs.

0.5.1 (2006-06-22):
  - Added hotfix for ``twisted.test.proto_helpers.StringTransport``.

0.5.0 (2006-06-12):
  - Replaced ``'%y'`` with ``'%Y'`` in ``Time.asHumanly`` output - the year is
    now four digits, rather than two.
  - Added new ``epsilon.structlike`` functionality for simple record.
  - All uses of ``defer.wait`` and ``deferredResult`` were removed from the tests.
  - Added ``epsilon.juice``, an asynchronous messaging protocol slated for
    inclusion in *Twisted*.  Improved a few features, such as the ``repr`` of
    ``JuiceBox`` instances.  This was moved from *Vertex*.
  - Added ``epsilon.sslverify``, a set of utilities for dealing with
    *PyOpenSSL* using simple high-level objects, performing operations such as
    signing and verifying certificates. This was also moved from *Vertex*, and
    slated for inclusion in *Twisted*.
  - Added ``epsilon.spewer``, a prettier version of the spewer in
    ``twisted.python.util``.
  - Added *benchmark* tool for measuring and reporting run-times of python
    programs.

0.4.0 (2005-12-20):
  - Disabled crazy ``sys.modules`` hackery in ``test_setuphelper``.
  - Added module for creating a directory structure from a string template.
  - Added support for *now* to ``Time.fromHumanly``.
  - Added a structured *hotfix* system to abstract and formalize monkey
    patches and version testing logic away from code which requires it.

0.3.2 (2005-11-05):
  - Added automatic support for *Twisted* plugins to ``autosetup``.

0.3.1 (2005-11-02):
  - Removed bogus dependency on *Axiom*.

0.3.0 (2005-11-02):
  - Added ``SchedulingService``, an ``IService`` implementation, to
    ``epsilon.cooperator``.
  - Added ``autosetup``, a utility to actually include files in *distutils*
    releases, to ``epsilon.setuphelper``.

0.2.1 (2005-10-25):
  - Added ``short`` to ``epsilon.versions.Version``.
  - Fixed *setup.py* to use ``epsilon.version.short`` rather than static
    string.

0.2.0 (2005-10-25):
  - Added ``epsilon.modal.ModalType``, metaclass for writing classes that
    behave in some respects like state machines.
