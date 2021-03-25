<?php

use Twig\Environment;
use Twig\Error\LoaderError;
use Twig\Error\RuntimeError;
use Twig\Extension\SandboxExtension;
use Twig\Markup;
use Twig\Sandbox\SecurityError;
use Twig\Sandbox\SecurityNotAllowedTagError;
use Twig\Sandbox\SecurityNotAllowedFilterError;
use Twig\Sandbox\SecurityNotAllowedFunctionError;
use Twig\Source;
use Twig\Template;

/* components/header.twig */
class __TwigTemplate_3c4093fa6c12fb18750f1cc7bc221064460a2e7d3db3b372a79b8f6f9892ea1f extends Template
{
    private $source;
    private $macros = [];

    public function __construct(Environment $env)
    {
        parent::__construct($env);

        $this->source = $this->getSourceContext();

        $this->parent = false;

        $this->blocks = [
        ];
    }

    protected function doDisplay(array $context, array $blocks = [])
    {
        $macros = $this->macros;
        // line 1
        echo "<header id=\"header\" class=\"bg-blue-600 shadow sticky top-0 dark:bg-purple-700\">
    <div class=\"border-b border-blue-700 dark:border-purple-800\">
        <div class=\"container flex flex-wrap justify-between items-center space-x-6 mx-auto p-4 md:flex-row xl:max-w-screen-xl\">
            <a href=\".\" class=\"flex items-center space-x-2 p-1\" title=\"";
        // line 4
        echo twig_escape_filter($this->env, call_user_func_array($this->env->getFunction('config')->getCallable(), ["site_title"]), "html", null, true);
        echo "\">
                <svg aria-hidden=\"true\" focusable=\"false\" data-prefix=\"fas\" data-icon=\"folder-tree\" class=\"inline-block fill-current text-white w-8 h-8\" role=\"img\" xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 576 512\">
                    <path fill=\"currentColor\" d=\"M544 32H432L400 0h-80a32 32 0 0 0-32 32v160a32 32 0 0 0 32 32h224a32 32 0 0 0 32-32V64a32 32 0 0 0-32-32zm0 288H432l-32-32h-80a32 32 0 0 0-32 32v160a32 32 0 0 0 32 32h224a32 32 0 0 0 32-32V352a32 32 0 0 0-32-32zM64 16A16 16 0 0 0 48 0H16A16 16 0 0 0 0 16v400a32 32 0 0 0 32 32h224v-64H64V160h192V96H64z\"></path>
                </svg>
            </a>

            <div class=\"flex-1 max-w-xl\">
                ";
        // line 11
        $this->loadTemplate("components/search.twig", "components/header.twig", 11)->display($context);
        // line 12
        echo "            </div>

            <div class=\"flex items-center justify-center w-6\">
                ";
        // line 15
        $this->loadTemplate("components/theme-toggle.twig", "components/header.twig", 15)->display($context);
        // line 16
        echo "            </div>
        </div>
    </div>

    <div class=\"border-t border-blue-500 dark:border-purple-600\">
        <div class=\"container flex flex-wrap justify-between items-center space-x-6 mx-auto px-4 py-1 md:flex-row xl:max-w-screen-xl\">
            ";
        // line 22
        $this->loadTemplate("components/breadcrumbs.twig", "components/header.twig", 22)->display($context);
        // line 23
        echo "
            ";
        // line 24
        if (((($context["path"] ?? null) &&  !twig_test_empty(($context["files"] ?? null))) && call_user_func_array($this->env->getFunction('config')->getCallable(), ["zip_downloads"]))) {
            // line 25
            echo "                <a href=\"";
            echo twig_escape_filter($this->env, call_user_func_array($this->env->getFunction('zip_url')->getCallable(), [($context["path"] ?? null)]), "html", null, true);
            echo "\" title=\"";
            echo twig_escape_filter($this->env, call_user_func_array($this->env->getFunction('translate')->getCallable(), ["download"]), "html", null, true);
            echo "\" rel=\"nofollow\"
                    class=\"flex justify-center  items-center text-sm text-white w-6 hover:text-gray-300\"
                >
                    <i class=\"fas fa-download fa-lg\"></i>
                </a>
            ";
        }
        // line 31
        echo "        </div>
    </div>
</header>
";
    }

    public function getTemplateName()
    {
        return "components/header.twig";
    }

    public function isTraitable()
    {
        return false;
    }

    public function getDebugInfo()
    {
        return array (  88 => 31,  76 => 25,  74 => 24,  71 => 23,  69 => 22,  61 => 16,  59 => 15,  54 => 12,  52 => 11,  42 => 4,  37 => 1,);
    }

    public function getSourceContext()
    {
        return new Source("", "components/header.twig", "/var/www/directorylister/app/views/components/header.twig");
    }
}
