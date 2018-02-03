from citizenshell import LocalShell, ShellError


def check_exception_is_not_raised(cmd, global_check_xc=False, local_check_xc=None,
                                  global_check_err=False, local_check_err=None):
    shell = LocalShell(check_xc=global_check_xc, check_err=global_check_err)
    shell(cmd, check_xc=local_check_xc, check_err=local_check_err)


def check_exception_is_raised(cmd, global_check_xc=False, local_check_xc=None,
                              global_check_err=False, local_check_err=None):
    exception_caught = None

    try:
        shell = LocalShell(check_xc=global_check_xc, check_err=global_check_err)
        shell(cmd, check_xc=local_check_xc, check_err=local_check_err)
    except ShellError as e:
        exception_caught = e

    assert exception_caught is not None


def test_local_shell_can_be_instantiated():
    LocalShell()


def test_local_shell_can_be_provided_with_a_specific_shell():
    LocalShell(shell="/bin/zsh")


def test_local_shell_can_run_one_basic_command():
    shell = LocalShell()
    result = shell("echo Foo")
    assert result == "Foo"


def test_local_shell_can_run_another_basic_command():
    shell = LocalShell()
    result = shell("echo Bar")
    assert result == "Bar"


def test_local_shell_result_has_stdout():
    shell = LocalShell()
    result = shell("echo Foo")
    assert result.out == ["Foo"]
    assert result.err == []
    assert result.xc == 0


def test_local_shell_result_has_stderr():
    shell = LocalShell()
    result = shell(">&2 echo Baz")
    assert result.out == []
    assert result.err == ["Baz"]
    assert result.xc == 0


def test_local_shell_result_has_exit_code():
    shell = LocalShell()
    result = shell("exit 15")
    assert result.out == []
    assert result.err == []
    assert result.xc == 15


def test_local_shell_result_can_be_compared_for_boolean():
    shell = LocalShell()
    assert shell("exit 0")
    assert not shell("exit 10")


def test_local_shell_result_can_be_iterated_on():
    shell = LocalShell()
    collected = []
    for line in shell("echo 'Foo\nBar'"):
        collected.append(line)
    assert collected == ['Foo', 'Bar']


def test_local_shell_has_environment_variable():
    shell = LocalShell()
    shell["SOME_VARIABLE"] = "value"
    assert shell["SOME_VARIABLE"] == "value"
    assert shell("echo $SOME_VARIABLE") == "value"


def test_local_shell_result_can_throw_on_nonzero_exitcode():
    check_exception_is_raised("exit 33", global_check_xc=True, local_check_xc=None)
    check_exception_is_raised("exit 33", global_check_xc=True, local_check_xc=True)
    check_exception_is_raised("exit 33", global_check_xc=False, local_check_xc=True)
    check_exception_is_not_raised("exit 33", global_check_xc=False, local_check_xc=None)


def test_local_shell_result_can_throw_on_nonempty_err():
    check_exception_is_raised(">&2 echo error", global_check_err=True, local_check_err=None)
    check_exception_is_raised(">&2 echo error", global_check_err=True, local_check_err=True)
    check_exception_is_raised(">&2 echo error", global_check_err=False, local_check_err=True)
    check_exception_is_not_raised(">&2 echo error", global_check_err=False, local_check_err=None)