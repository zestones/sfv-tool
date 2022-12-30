# sfv-tool

**Simple file verification** (SFV) is a file format for storing CRC32 checksums of files to verify the integrity of files. SFV is used to verify that a file has not been corrupted, but it does not otherwise verify the file's authenticity. The .sfv file extension is usually used for SFV files. ([wikipedia](https://en.wikipedia.org/wiki/Simple_file_verification))

This repository is composed of two script : ``sfv-generator.py`` and ``sfv-validator.py``.
 
 * [sfv-generator](https://github.com/zestones/sfv-tool/tree/main/sfv-generator) : generate SFV for your files.
 * [sfv-validator](https://github.com/zestones/sfv-tool/tree/main/sfv-validator) : verify that your files has not been corrupted.