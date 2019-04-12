#!/usr/bin/env python
#
# Copyright 2019 The Nakama Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os

cur_dir = os.path.abspath('.')
roots_pem_path = os.path.join(cur_dir, '../third_party/grpc/etc/roots.pem')
out_h_path     = os.path.join(cur_dir, '../src/roots_pem.h')
out_cpp_path   = os.path.join(cur_dir, '../src/roots_pem.cpp')

def write_head(f):
    f.write('// file generated by conv_roots_pem.py\n\n')

in_file = open(roots_pem_path, 'r')
out_cpp_file = open(out_cpp_path, 'w')

count = 0
max_line_size = 80
count_in_line = 0

write_head(out_cpp_file)
out_cpp_file.write('#ifdef NAKAMA_SSL_ENABLED\n\n')
out_cpp_file.write('#include "roots_pem.h"\n\n')
out_cpp_file.write('const unsigned char g_roots_pem_buff[] = {\n')

while True:
    data = in_file.read(1024)

    if not data:
        break # end of file

    for c in data:
        if count > 0:
            out_cpp_file.write(',')
        out_cpp_file.write(hex(ord(c)))
        count += 1
        count_in_line += 1
        if count_in_line >= max_line_size:
            count_in_line = 0
            out_cpp_file.write('\n')

out_cpp_file.write(',0};\n\n')

out_cpp_file.write('const char* g_roots_pem = (const char*)g_roots_pem_buff;\n')
out_cpp_file.write('const uint32_t g_roots_pem_size = sizeof(g_roots_pem_buff) - 1;\n')
out_cpp_file.write('\n#endif // NAKAMA_SSL_ENABLED\n')

in_file.close()
out_cpp_file.close()

out_h_file = open(out_h_path, 'w')
write_head(out_h_file)
out_h_file.write('#pragma once\n\n')
out_h_file.write('#include <cstdint>\n\n')
out_h_file.write('extern const char* g_roots_pem;\n')
out_h_file.write('extern const uint32_t g_roots_pem_size;\n')
out_h_file.close()