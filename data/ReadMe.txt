VII/237             HYPERLEDA. I. Catalog of galaxies        (Paturel+, 2003)
================================================================================
HYPERLEDA. I. Identification and designation of galaxies.
    Paturel G., Petit C., Prugniel P., Theureau G., Rousseau J., Brouty M.,
    Dubois P., Cambresy L.
   <Astron. Astrophys. 412, 45 (2003)>
   =2003A&A...412...45P
================================================================================
ADC_Keywords: Galaxy catalogs
Keywords: galaxies: general - catalogs

Abstract:
    We present the new catalog of principal galaxies (PGC2003). It
    constitutes the framework of the HYPERLEDA database that supersedes
    the LEDA one, with more data and more capabilities. The catalog is
    still restricted to confirmed galaxies, i.e. about one million
    galaxies, brighter than ~18B-mag.

    In order to provide the best possible identification for each galaxy
    we give: accurate coordinates (typical accuracy better than 2 arcsec),
    diameter, axis ratio and position angle. Diameters and axis ratios
    have been homogenized to the RC2 system at the limiting surface
    brightness of 25B-mag/arcsec^2^, using a new method, the EPIDEMIC
    method.

    In order to provide the best designation for each galaxy, we collected
    the names from 50 catalogues. The compatibility of the spelling is
    tested against NED and SIMBAD, and, as far as possible we used a
    spelling compatible with both. For some cases, where no consensus
    exists between NED, SIMBAD and LEDA, we propose some changes that
    could make the spelling of names fully compatible.

    The full catalog is distributed through the CDS and can be extracted
    from HYPERLEDA, http://leda.univ-lyon1.fr/ .

File Summary:
--------------------------------------------------------------------------------
 FileName      Lrecl  Records   Explanations
--------------------------------------------------------------------------------
ReadMe            80        .   This file
pgc.dat          342   983261   Catalog of galaxies (table 5 in the paper)
accro.dat         80       50   Table of adopted acronyms (table 2 in the paper)
--------------------------------------------------------------------------------

See also:
    http://leda.univ-lyon1.fr/ : the Hyperleda Home Page
    VII/238 : HYPERLEDA. II. Catalog of homogenized HI data (Paturel+, 2003)

Byte-by-byte Description of file: pgc.dat
--------------------------------------------------------------------------------
   Bytes Format Units        Label   Explanations
--------------------------------------------------------------------------------
   1-  3  A3    ---          ---     [PCG]
   4- 10  I7    ---          PGC     [1/3099300] PGC number
      12  A1    ---          ---     [J]
  13- 14  I2    h            RAh     Right ascension (J2000)
  15- 16  I2    min          RAm     Right ascension (J2000)
  17- 20  F4.1  s            RAs     Right ascension (J2000)
      21  A1    ---          DE-     Declination sign (J2000)
  22- 23  I2    deg          DEd     Declination (J2000)
  24- 25  I2    arcmin       DEm     Declination (J2000)
  26- 27  I2    arcsec       DEs     Declination (J2000)
  29- 30  A2    ---          OType   [GM ] Object type (1)
  32- 36  A5    ---          MType   Provisional morphological type from LEDA
                                      according to the RC2 code.
  37- 41  F5.2 [0.1arcmin]   logD25  ?=9.99 Apparent diameter (2)
  42- 44  A3    ---          ---     [+/-]
  45- 48  F4.2 [0.1arcmin] e_logD25  ?=9.99 Actual error of logD25
  51- 54  F4.2  [---]        logR25  ?=9.99 Axis ratio in log scale
                                       (log of major axis to minor axis)
  55- 57  A3    ---          ---     [+/-]
  58- 61  F4.2  [---]      e_logR25  ?=9.99 Actual error on logR25
  64- 67  F4.0  deg          PA      ?=999. Adopted 1950-position angle (3)
  68- 70  A3    ---          ---     [+/-]
  71- 74  F4.0  deg        e_PA      ?=999. rms uncertainty on PA
  76- 77  I2    ---        o_ANames  Number of alternate names.
  79-341  A263  ---          ANames  Alternate names (4)
--------------------------------------------------------------------------------
Note (1): 'G', galaxies; 'M', multiple system; GM, galaxy in multiple system.

Note (2): Apparent diameter in log scale (D in 0.1arcmin) converted to the
    RC3 system at the isophote 25B-mag/arcsec^2^ (section 3);

Note (3): Adopted 1950-position angle, measured from the North to the East.
    Its value covers the range 0-180. A few values exactly equal to zero
    are taken as 180.

Note (4): Alternate names following the hierarchy given in accro.dat file.
    Up to 12 names, each 22 bytes long, is given here.
    Names that correspond to a multiple system are written in parenthesis.
    151 Names that do not agree with NED identification have been written
    with a question mark (?). 677 names that have been moved from one
    galaxy to another since the first catalog have been written with an
    exclamation point (!).
--------------------------------------------------------------------------------

Byte-by-byte Description of file: accro.dat
--------------------------------------------------------------------------------
   Bytes Format Units   Label     Explanations
--------------------------------------------------------------------------------
   1- 23  A23   ---     Name      Example of the name (1)
  25- 51  A27   ---     Aut       Authors' name
  53- 82  A30   ----    Ref       BibCode or catalog number
--------------------------------------------------------------------------------
Note (1): For each adopted acronym we give an example of a name and the
    reference where the acronym was created. When an acronym comes from
    several references (e.g., KUG), we give the latest reference that
    lists the former ones.
--------------------------------------------------------------------------------

Acknowledgements: Georges Paturel <patu@obs.univ-lyon1.fr>
================================================================================
(End)                                        Patricia Bauer [CDS]    28-Nov-2003
